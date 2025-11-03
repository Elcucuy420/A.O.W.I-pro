import os, httpx
CALCOM_WEBHOOK = os.getenv("CALCOM_WEBHOOK", "")
GOOGLE_CAL_WEBHOOK = os.getenv("GOOGLE_CAL_WEBHOOK", "")

async def propose_booking(payload: dict) -> bool:
    url = CALCOM_WEBHOOK or GOOGLE_CAL_WEBHOOK
    if not url: return False
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)
        return r.status_code < 300
