import os, time
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from core.config import settings

ALGO = 'HS256'
HTTP_BEARER = HTTPBearer(auto_error=True)

def _secret() -> str:
    # In prod, set ADMIN_JWT_SECRET in env; fallback for dev only
    return os.getenv('ADMIN_JWT_SECRET', 'dev-secret-change-me')

def create_admin_token(subject: str = 'admin', ttl_seconds: int = 86400) -> str:
    now = int(time.time())
    payload = {'sub': subject, 'iat': now, 'exp': now + ttl_seconds, 'scope': 'admin'}
    return jwt.encode(payload, _secret(), algorithm=ALGO)

def verify_admin_token(token: str) -> dict:
    try:
        data = jwt.decode(token, _secret(), algorithms=[ALGO])
        if data.get('scope') != 'admin':
            raise HTTPException(status_code=403, detail='Invalid scope')
        return data
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

async def require_admin(creds: HTTPAuthorizationCredentials = Depends(HTTP_BEARER)):
    return verify_admin_token(creds.credentials)
