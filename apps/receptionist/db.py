from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_async_engine(settings.LEADS_DB_URL, future=True, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    channel: str
    caller: str
    intent: str
    note: str
