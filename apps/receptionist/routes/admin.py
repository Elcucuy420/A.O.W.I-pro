from fastapi import APIRouter, Depends
from core.security import create_admin_token, require_admin
from services.storage import export_leads

router = APIRouter()

@router.post('/login')
async def login():
    # In production, replace with real identity provider or password check.
    # This issues a short-lived admin token for operator use.
    token = create_admin_token()
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/leads')
async def admin_leads(_=Depends(require_admin)):
    return await export_leads()
