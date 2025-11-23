from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import os
import json
import redis.asyncio as aioredis
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CHANNEL = "trade_events"

class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return  # No one to send to
        
        data = json.dumps(message)
        dead = []
        for ws in self.active_connections:
            try:
                await ws.send_text(data)
            except Exception as e:
                logger.warning(f"Failed to send to websocket: {e}")
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()
_listener_task = None


async def redis_listener():
    """
    Background task: listens to Redis Pub/Sub and broadcasts messages to WebSocket clients.
    Includes reconnection logic for reliability.
    """
    client = None
    pubsub = None
    reconnect_delay = 1
    max_reconnect_delay = 30
    
    while True:
        try:
            # Create Redis connection
            if client is None:
                client = aioredis.from_url(
                    f"redis://{REDIS_HOST}:{REDIS_PORT}",
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                logger.info(f"🔌 Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            
            # Create pubsub and subscribe
            if pubsub is None:
                pubsub = client.pubsub()
                await pubsub.subscribe(CHANNEL)
                logger.info(f"📡 Subscribed to Redis channel: {CHANNEL}")
                reconnect_delay = 1  # Reset delay on successful connection
            
            # Listen for messages
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    try:
                        data = json.loads(msg["data"])
                        logger.debug(f"📨 Received message from Redis: {data}")
                        await manager.broadcast(data)
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Failed to parse message: {e}")
                    except Exception as e:
                        logger.error(f"❌ Error broadcasting message: {e}")
                        
        except (ConnectionError, OSError, TimeoutError) as e:
            logger.error(f"❌ Redis connection error: {e}. Reconnecting in {reconnect_delay}s...")
            # Clean up connections
            if pubsub:
                try:
                    await pubsub.unsubscribe(CHANNEL)
                    await pubsub.close()
                except:
                    pass
                pubsub = None
            if client:
                try:
                    await client.close()
                except:
                    pass
                client = None
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, max_reconnect_delay)  # Exponential backoff
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in Redis listener: {e}")
            # Clean up connections
            if pubsub:
                try:
                    await pubsub.unsubscribe(CHANNEL)
                    await pubsub.close()
                except:
                    pass
                pubsub = None
            if client:
                try:
                    await client.close()
                except:
                    pass
                client = None
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, max_reconnect_delay)


async def start_redis_listener():
    """
    Start the Redis listener task. Should be called at application startup.
    """
    global _listener_task
    if _listener_task is None or _listener_task.done():
        _listener_task = asyncio.create_task(redis_listener())
        logger.info("🚀 Redis listener task started")
    return _listener_task


async def stop_redis_listener():
    """
    Stop the Redis listener task. Should be called at application shutdown.
    """
    global _listener_task
    if _listener_task and not _listener_task.done():
        _listener_task.cancel()
        try:
            await _listener_task
        except asyncio.CancelledError:
            pass
        logger.info("🛑 Redis listener task stopped")


@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            # Keep connection alive and handle any incoming messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
