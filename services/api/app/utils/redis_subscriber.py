import os
import redis.asyncio as aioredis
import json

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

async def redis_subscriber():
    """
    Async generator for subscribing to trade events from Redis
    """
    client = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    pubsub = client.pubsub()
    await pubsub.subscribe("trade_events")

    async for message in pubsub.listen():
        if message["type"] == "message":
            yield json.loads(message["data"])
