from beanie import Document
from datetime import datetime
from pydantic import Field
import uuid

class TradeDocument(Document):
    id : uuid.UUID = Field(default_factory=uuid.uuid4)
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

