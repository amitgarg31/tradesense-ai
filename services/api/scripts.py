from app.core.db_session import engine
from app.models.trade_model import SQLModel

def init_db():
    print("📦 Creating tables if not exist...")
    SQLModel.metadata.create_all(engine)
    print("✅ Database ready!")

if __name__ == "__main__":
    init_db()
