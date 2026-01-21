# ORM (Object Relational Mapping) lets us interact with relational databases using Python objects instead of raw SQL

from collections.abc import AsyncGenerator
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine,expire_on_commit = False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_sessionmaker() as session:
        yeild session 
