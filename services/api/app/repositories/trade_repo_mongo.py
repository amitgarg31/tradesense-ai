from datetime import datetime

from app.models.trade_mongo import TradeDocument


async def save_trade_to_mongo(symbol: str, price: float, timestamp: datetime = None):
    # Use provided timestamp or create a new one (fallback)
    if timestamp is None:
        timestamp = datetime.utcnow()

    trade = TradeDocument(symbol=symbol, price=price, timestamp=timestamp)
    await trade.insert()
    print(f"✅ Saved {symbol} to MongoDB (Beanie) at {timestamp.isoformat()}")
