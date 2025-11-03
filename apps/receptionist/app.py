import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.voice import router as voice_router
from routes.messages import router as messages_router
from routes.chat import router as chat_router

app = FastAPI(title="AI Receptionist (Norway-first)")

allowed = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "service": "ai-receptionist"}

app.include_router(voice_router, prefix="/twilio", tags=["twilio"])
app.include_router(messages_router, prefix="/twilio", tags=["twilio"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
