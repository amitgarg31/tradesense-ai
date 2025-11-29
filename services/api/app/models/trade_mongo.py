import uuid
from datetime import datetime

from beanie import Document
from pydantic import Field


class TradeDocument(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    symbol: str
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "trades"


class SummaryDocument(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    symbol: str
    summary: str
    embedding: list[float]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "llm_summaries"
