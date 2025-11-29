from datetime import datetime

from sqlmodel import Field, SQLModel


class Trade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(max_length=10, index=True)
    price: float
    processed_at: datetime = Field(default_factory=datetime.utcnow)
