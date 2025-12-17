import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Async Config
DATABASE_URL_ASYNC = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql" in DATABASE_URL else DATABASE_URL

engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync Config (for sync routers)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure sync url
DATABASE_URL_SYNC = DATABASE_URL.replace("+asyncpg", "") # Remove async driver if present
engine_sync = create_engine(DATABASE_URL_SYNC, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_db_sync():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
