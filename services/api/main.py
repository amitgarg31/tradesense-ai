from fastapi import FastAPI
from services.api.app.routes import ingest, query, insights
from services.api.app.core.mongo_orm import init_mongo
from services.api.app.core.db_session import init_db
from services.api.app.routes.ws import router as ws_router, start_redis_listener, stop_redis_listener

app = FastAPI(title="TradeSense AI", version="1.0")

@app.on_event("startup")
async def on_startup():
    init_db()          # PostgreSQL ORM init
    await init_mongo() # Mongo ODM init
    await start_redis_listener()  # Start Redis Pub/Sub listener for WebSocket

@app.on_event("shutdown")
async def on_shutdown():
    await stop_redis_listener()  # Stop Redis listener gracefully

app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(ws_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
