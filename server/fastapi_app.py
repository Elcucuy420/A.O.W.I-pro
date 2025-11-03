from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import core logic and integrations. These imports will work when running
# within the project structure where `core` and `integrations` are packages.
from core.agent import AIReceptionistAgent

# Initialize FastAPI app and AI agent
app = FastAPI(title="AI Receptionist API")
agent = AIReceptionistAgent()

class MessageRequest(BaseModel):
    """
    Request model representing an incoming chat message from a user. The
    `user_id` should uniquely identify the user or session so the agent can
    maintain context between messages.
    """
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: MessageRequest) -> dict:
    """
    Endpoint for sending a user message to the AI receptionist agent. Returns
    the agent's reply. If an error occurs during processing, a 500 HTTP error
    will be returned with the exception message.
    """
    try:
        response_text = agent.handle_message(request.user_id, request.message)
    except Exception as exc:  # Catch generic exceptions to surface them in the API
        raise HTTPException(status_code=500, detail=str(exc))
    return {"reply": response_text}
