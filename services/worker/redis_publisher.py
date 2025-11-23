import json
import os
import redis

# Connect to Redis inside Docker (use service name)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Create Redis client with connection pooling and error handling
redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)

def publish_trade_event(event: dict):
    """
    Publish processed trade event to Redis Pub/Sub channel
    """
    try:
        # Test connection first
        redis_client.ping()
        
        # Publish the event
        message = json.dumps(event)
        subscribers = redis_client.publish("trade_events", message)
        print(f"📢 Published trade event to Redis: {event['symbol']} @ {event['price']} (subscribers: {subscribers})")
        return subscribers
    except redis.ConnectionError as e:
        print(f"❌ Redis connection error: {e}")
        print(f"   Trying to connect to {REDIS_HOST}:{REDIS_PORT}")
        raise
    except redis.TimeoutError as e:
        print(f"❌ Redis timeout error: {e}")
        raise
    except Exception as e:
        print(f"❌ Error publishing to Redis: {e}")
        raise
