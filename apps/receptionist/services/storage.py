import json, os, time, threading
from pathlib import Path

STORE = Path(os.getenv("LEADS_DIR", "leads"))
STORE.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()

def persist_lead(lead: dict):
    if not lead: return
    ts = time.strftime("%Y%m%d-%H%M%S")
    p = STORE / f"lead-{ts}.json"
    with _lock, open(p, "w", encoding="utf-8") as f:
        json.dump(lead, f, ensure_ascii=False, indent=2)

def export_leads():
    out = []
    for p in sorted(STORE.glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return {"count": len(out), "leads": out}
