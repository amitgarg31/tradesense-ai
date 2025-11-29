from datetime import datetime

from sqlmodel import Session

from app.models.trade_sql import Trade


def save_trade_to_postgres(
    session: Session, symbol: str, price: float, timestamp: datetime = None
):
    # Use provided timestamp or create a new one (fallback)
    if timestamp is None:
        timestamp = datetime.utcnow()

    trade = Trade(symbol=symbol, price=price, processed_at=timestamp)
    session.add(trade)
    session.commit()
    print(f"✅ Saved {symbol} to PostgreSQL at {timestamp.isoformat()}")
