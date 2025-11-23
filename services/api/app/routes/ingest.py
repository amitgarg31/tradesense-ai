from fastapi import APIRouter, BackgroundTasks
from services.api.app.utils.producer import send_to_queue
from datetime import datetime
router = APIRouter()

@router.post("/")
async def ingest_data(symbol: str, price: float, background_tasks: BackgroundTasks):
    # Create a single UTC timestamp at ingestion time
    timestamp = datetime.utcnow()
    # Convert to ISO format string for JSON serialization
    data = {
        "symbol": symbol, 
        "price": price, 
        "timestamp": timestamp.isoformat()
    }
    background_tasks.add_task(send_to_queue, data)
    return {"status": "received", "data": {**data, "timestamp": timestamp.isoformat()}}
