import pymysql

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import QueuePool

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
ASYNC_SQLALCHEMY_DATABASE_URL = settings.ASYNC_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool, pool_size=100
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,     poolclass=QueuePool, pool_size=100)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_async_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
