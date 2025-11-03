from fastapi import APIRouter, Request, Response
from services.guard import verify_twilio_signature_if_enabled
from services.llm import ai_reception_reply
from services.storage import persist_lead

router = APIRouter()

def twiml_say(text: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="nb-NO" voice="Polly.Liv">{text}</Say>
  <Pause length="1"/>
  <Say language="nb-NO" voice="Polly.Liv">
    Hvis du vil bli oppringt, si navnet ditt, hva du trenger hjelp med, og telefonnummer.
  </Say>
  <Record maxLength="60" playBeep="true" trim="trim-silence" />
</Response>
"""

@router.post("/voice", response_class=Response)
async def inbound_voice(request: Request):
    await verify_twilio_signature_if_enabled(request)
    form = await request.form()
    transcript_like = form.get("SpeechResult") or form.get("Digits") or ""
    caller = form.get("From", "")
    called = form.get("To", "")

    reply, lead = await ai_reception_reply(
        user_text=transcript_like, channel="voice", caller=caller, callee=called, locale_hint="nb-NO"
    )
    if lead: persist_lead(lead)
    xml = twiml_say(reply)
    return Response(content=xml, media_type="application/xml")
