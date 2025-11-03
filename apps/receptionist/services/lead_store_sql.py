from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal, Lead

async def save_lead(channel: str, caller: str, intent: str, note: str):
    async with SessionLocal() as session:
        try:
            lead = Lead(channel=channel, caller=caller, intent=intent, note=note)
            session.add(lead)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            pass

async def list_leads():
    async with SessionLocal() as session:
        res = await session.exec(select(Lead))
        return res.all()
