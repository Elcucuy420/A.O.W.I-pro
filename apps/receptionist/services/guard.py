import base64, hmac, hashlib
from fastapi import Request, HTTPException
from core.config import settings

def _compute_sig(url: str, params: dict) -> str:
    s = url + ''.join(k + v for k, v in sorted(params.items()))
    mac = hmac.new((settings.TWILIO_AUTH_TOKEN or '').encode(), s.encode(), hashlib.sha1).digest()
    return base64.b64encode(mac).decode()

async def verify_twilio_signature_if_enabled(request: Request):
    if not settings.VERIFY_TWILIO_SIGNATURE or not settings.TWILIO_AUTH_TOKEN:
        return
    signature = request.headers.get('X-Twilio-Signature')
    if not signature:
        raise HTTPException(status_code=403, detail='Missing Twilio signature')
    form = await request.form()
    expected = _compute_sig(str(request.url), dict(form))
    if signature != expected:
        raise HTTPException(status_code=403, detail='Bad Twilio signature')
