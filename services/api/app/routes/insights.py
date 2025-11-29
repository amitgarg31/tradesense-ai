from fastapi import APIRouter, HTTPException

from app.models.trade_mongo import SummaryDocument
from app.utils.producer import celery

router = APIRouter()


@router.get("/latest")
async def get_latest_summary(symbol: str = None):
    query = SummaryDocument.find_all()
    if symbol:
        query = SummaryDocument.find(SummaryDocument.symbol == symbol)

    summary = await query.sort("-timestamp").first_or_none()

    if not summary:
        raise HTTPException(status_code=404, detail="No summary found")

    return summary


@router.post("/trigger")
async def trigger_summary_generation(symbol: str):
    # Manually trigger the celery task
    task = celery.send_task("tasks.generate_summary", args=[symbol])
    return {"status": "triggered", "task_id": task.id, "symbol": symbol}
