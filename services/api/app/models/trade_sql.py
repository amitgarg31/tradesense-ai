from sqlmodel import SQLModel, Field
from datetime import datetime

class Trade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(max_length=10, index=True)
    price: float
    processed_at: datetime = Field(default_factory=datetime.utcnow)
