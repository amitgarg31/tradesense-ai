import os

from sqlmodel import Session, SQLModel, create_engine

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "tradesense")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)


# Dependency injection for FastAPI routes (if needed later)
def get_session():
    with Session(engine) as session:
        yield session


# ✅ Add this function to initialize your PostgreSQL tables
def init_db():
    """Create database tables if they don't exist."""

    print("📦 Initializing PostgreSQL tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ PostgreSQL tables are ready!")
