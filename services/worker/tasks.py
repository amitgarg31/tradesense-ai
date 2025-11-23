from celery import shared_task
import asyncio
from datetime import datetime
from services.api.app.core.db_session import engine
from sqlmodel import Session
from services.api.app.repositories.trade_repo_sql import save_trade_to_postgres
from services.api.app.repositories.trade_repo_mongo import save_trade_to_mongo
from services.api.app.core.mongo_orm import init_mongo
from services.worker.redis_publisher import publish_trade_event
import time


@shared_task(name="tasks.process_data")
def process_data(data):
    try:
        symbol = data["symbol"]
        price = data["price"]
        
        # Parse timestamp from ISO format string (created at ingestion)
        timestamp_str = data.get("timestamp")
        if timestamp_str:
            # Parse ISO format string back to datetime
            if isinstance(timestamp_str, str):
                try:
                    # Handle ISO format with or without timezone
                    if timestamp_str.endswith('Z'):
                        timestamp_str = timestamp_str.replace('Z', '+00:00')
                    timestamp = datetime.fromisoformat(timestamp_str)
                    # Ensure it's timezone-naive UTC (consistent with utcnow())
                    if timestamp.tzinfo is not None:
                        timestamp = timestamp.replace(tzinfo=None)
                except (ValueError, AttributeError) as e:
                    print(f"⚠️  Warning: Failed to parse timestamp '{timestamp_str}': {e}, using current time")
                    timestamp = datetime.utcnow()
            else:
                # Fallback if it's already a datetime object
                timestamp = timestamp_str
        else:
            # Fallback: create new timestamp if not provided
            timestamp = datetime.utcnow()
            print(f"⚠️  Warning: No timestamp in data, using current time")
        
        print(f"⚙️ Processing data: {symbol} @ {price} (timestamp: {timestamp.isoformat()})")
        
        # Simulate heavy processing
        time.sleep(2)
        
        # Save to databases asynchronously with consistent timestamp
        asyncio.run(save_to_databases(symbol, price, timestamp))
        
        # Publish event to Redis Pub/Sub with the same timestamp
        try:
            publish_trade_event({
                "symbol": symbol,
                "price": price,
                "timestamp": timestamp.isoformat()  # Use ISO format for JSON
            })
        except Exception as redis_error:
            print(f"⚠️  Warning: Failed to publish to Redis: {redis_error}")
            # Don't fail the entire task if Redis publish fails
            # The data is already saved to databases
        
        print(f"✅ Completed {symbol}")
        return {"status": "completed", "symbol": symbol}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "failed", "error": str(e)}

async def save_to_databases(symbol: str, price: float, timestamp: datetime):
    # Init Mongo
    await init_mongo()
    await save_trade_to_mongo(symbol, price, timestamp)

    # Save to Postgres
    with Session(engine) as session:
        save_trade_to_postgres(session, symbol, price, timestamp)