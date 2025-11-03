import json, os, time, asyncio
from pathlib import Path
from services.lead_store_sql import save_lead, list_leads

STORE = Path(os.getenv('LEADS_DIR', 'leads'))
STORE.mkdir(parents=True, exist_ok=True)

def persist_lead(lead: dict):
    """
    Persist to filesystem for audit, then enqueue async DB write.
    Safe to call from sync FastAPI handlers.
    """
    if not lead: return
    ts = time.strftime('%Y%m%d-%H%M%S')
    p = STORE / f'lead-{ts}.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(lead, f, ensure_ascii=False, indent=2)
    # Schedule async DB save
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(save_lead(lead.get('channel',''), lead.get('caller',''), lead.get('intent',''), lead.get('note','')))
    except RuntimeError:
        # No loop; ignore (file backup already exists)
        pass

async def export_leads():
    try:
        rows = await list_leads()
        return {'count': len(rows), 'leads': [r.model_dump() for r in rows]}
    except Exception:
        # Fallback: read from files if DB unavailable
        out = []
        for p in sorted(STORE.glob('*.json')):
            try:
                out.append(json.loads(p.read_text(encoding='utf-8')))
            except Exception:
                pass
        return {'count': len(out), 'leads': out}
