import os

import motor.motor_asyncio
from beanie import init_beanie

from app.models.trade_mongo import SummaryDocument, TradeDocument


async def init_mongo():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017") or os.getenv(
        "MONGO_URI_LOCAL"
    )
    mongo_db = os.getenv("MONGO_DB", "tradesense_ai")
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    await init_beanie(
        database=client[mongo_db], document_models=[TradeDocument, SummaryDocument]
    )
    print("✅ MongoDB (Beanie) initialized")
