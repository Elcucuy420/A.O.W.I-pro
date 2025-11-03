# AI Receptionist (Norway-first)

FastAPI microservice for Twilio Voice/SMS/WhatsApp + web chat.
Norwegian by default; auto language switch. Booking webhooks + JSON lead capture.

## Local
uvicorn app:app --reload --host 0.0.0.0 --port 8000

## Twilio
- Voice webhook → POST /twilio/voice
- WhatsApp/SMS → POST /twilio/messages

## Chat widget
Open /chat/widget

## Env
Copy .env.example → .env and fill secrets.

## Docker
docker build -t ai-receptionist .
docker run -p 8000:8000 --env-file .env ai-receptionist
