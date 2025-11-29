from fastapi import APIRouter

from app.models.trade_mongo import TradeDocument

router = APIRouter()


@router.get("/")
async def query_trades(symbol: str, limit: int = 5):
    results = (
        await TradeDocument.find(TradeDocument.symbol == symbol)
        .sort("-timestamp")
        .limit(limit)
        .to_list()
    )
    return {"symbol": symbol, "recent_trades": results}
