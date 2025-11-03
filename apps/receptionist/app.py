import os, logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routes.voice import router as voice_router
from routes.messages import router as messages_router
from routes.chat import router as chat_router
from routes.admin import router as admin_router
from core.config import settings
from core.observability import CorrelationIdMiddleware, metrics_router
from core.logging import setup_logging
from db import init_db

try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    from slowapi.middleware import SlowAPIMiddleware
    limiter = Limiter(key_func=get_remote_address)
except Exception:
    limiter = None

setup_logging()
app = FastAPI(title='AI Receptionist (Norway-first)', version='1.1.0')

allowed = settings.ALLOWED_ORIGINS.split(',') if settings.ALLOWED_ORIGINS else ['*']
app.add_middleware(CORSMiddleware, allow_origins=allowed, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(CorrelationIdMiddleware)

if limiter and settings.ENABLE_RATE_LIMIT:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

@app.on_event('startup')
async def _startup():
    await init_db()

@app.get('/health')
async def health():
    return {'ok': True, 'env': settings.ENV}

@app.get('/')
def root():
    return {'ok': True, 'service': 'ai-receptionist'}

# Routers
app.include_router(voice_router, prefix='/twilio', tags=['twilio'])
app.include_router(messages_router, prefix='/twilio', tags=['twilio'])
app.include_router(chat_router, prefix='/chat', tags=['chat'])
app.include_router(admin_router, prefix='/admin', tags=['admin'])
app.include_router(metrics_router, tags=['metrics'])
