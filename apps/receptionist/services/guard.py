import os, hmac, hashlib, base64
from fastapi import Request, HTTPException

TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
VERIFY_TWILIO_SIGNATURE = os.getenv("VERIFY_TWILIO_SIGNATURE", "false").lower() == "true"

def _compute_sig(url: str, params: dict) -> str:
    s = url + "".join(k + v for k, v in sorted(params.items()))
    mac = hmac.new(TWILIO_AUTH_TOKEN.encode(), s.encode(), hashlib.sha1).digest()
    return base64.b64encode(mac).decode()

async def verify_twilio_signature_if_enabled(request: Request):
    if not VERIFY_TWILIO_SIGNATURE or not TWILIO_AUTH_TOKEN:
        return
    signature = request.headers.get("X-Twilio-Signature")
    if not signature:
        raise HTTPException(status_code=403, detail="Missing Twilio signature")
    form = await request.form()
    expected = _compute_sig(str(request.url), dict(form))
    if signature != expected:
        raise HTTPException(status_code=403, detail="Bad Twilio signature")
