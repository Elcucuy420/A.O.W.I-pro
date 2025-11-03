import os, httpx
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = open("prompts/receptionist_nb.txt", "r", encoding="utf-8").read()

async def call_openai(messages):
    if not OPENAI_API_KEY:
        return "Hei! (dev) Hvordan kan jeg hjelpe deg i dag?"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"model": OPENAI_MODEL, "messages": messages, "temperature": 0.3}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

def extract_lead_struct(text: str, channel: str, caller: str):
    if any(k in (text or "").lower() for k in ["time", "booking", "bestille", "consult", "appointment"]):
        return {"channel": channel, "caller": caller, "intent": "booking_or_consult", "note": (text or "")[:600]}
    return None

async def ai_reception_reply(user_text: str, channel: str, caller: str, callee: str, locale_hint: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"[{locale_hint}] Channel={channel} From={caller} To={callee}\nUser: {user_text or ''}"},
    ]
    reply = await call_openai(messages)
    lead = extract_lead_struct(user_text, channel, caller)
    return reply, lead
