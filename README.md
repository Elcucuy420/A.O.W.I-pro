# AI Receptionist

This repository provides a modular scaffold for an AI receptionist designed for Norwegian small businesses.  It uses Python and FastAPI to expose a webhook and chat interface that can integrate with calendars, email, invoicing and payments through configuration files.

## Project layout

- **config/** – JSON files describing business details, opening hours and which integrations are enabled.
- **core/** – the conversational agent, intent router and in‑memory session manager.
- **integrations/** – stubs for Google Calendar, Gmail, Tripletex and Vipps.  These files can be extended to call real APIs.
- **server/** – a FastAPI application exposing a `/chat` endpoint and a basic webhook receiver.

## Running locally

1. Install Python 3.10+ and create a virtual environment.
2. Install the dependencies listed in `requirements.txt`.
3. Set your OpenAI API key and any integration secrets as environment variables.
4. Start the server with `uvicorn server.fastapi_app:app --reload`.
5. POST JSON to `/chat` with a `message` property to interact with the agent.

## Notes

This scaffold intentionally leaves many functions as stubs so you can integrate with your own services.  It is not production‑ready but provides a clear starting point.
