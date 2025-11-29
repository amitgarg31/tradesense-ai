from app.core.db_session import init_db
from app.core.mongo_orm import init_mongo
from app.routes import ingest, insights, market, query
from app.routes.ws import router as ws_router
from app.routes.ws import start_redis_listener, stop_redis_listener
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TradeSense AI", version="1.0")

# CORS Configuration for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    init_db()  # PostgreSQL ORM init
    await init_mongo()  # Mongo ODM init
    await start_redis_listener()  # Start Redis Pub/Sub listener for WebSocket


@app.on_event("shutdown")
async def on_shutdown():
    await stop_redis_listener()  # Stop Redis listener gracefully


app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(market.router, prefix="/market", tags=["Market Data"])
app.include_router(ws_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
