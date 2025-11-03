from fastapi import APIRouter, Request
from services.guard import verify_twilio_signature_if_enabled
from services.llm import ai_reception_reply
from services.storage import persist_lead

router = APIRouter()

@router.post("/messages")
async def inbound_message(request: Request):
    await verify_twilio_signature_if_enabled(request)
    form = await request.form()
    body = form.get("Body", "")
    wa_from = form.get("From", "")
    wa_to = form.get("To", "")

    reply, lead = await ai_reception_reply(
        user_text=body, channel="whatsapp_or_sms", caller=wa_from, callee=wa_to, locale_hint="nb-NO"
    )
    if lead: persist_lead(lead)
    return {"message": reply}
