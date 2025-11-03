from fastapi import APIRouter, Request
from services.llm import ai_reception_reply
from services.storage import persist_lead, export_leads

router = APIRouter()

@router.post("")
async def web_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    reply, lead = await ai_reception_reply(
        user_text=msg, channel="web_chat", caller="web", callee="agent", locale_hint="nb-NO"
    )
    if lead: persist_lead(lead)
    return {"reply": reply}

@router.get("/widget")
async def widget():
    return open("static/chat.html", "r", encoding="utf-8").read()

@router.get("/leads")
async def leads_dump():
    return export_leads()
