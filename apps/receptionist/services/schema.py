from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadCapture(BaseModel):
    channel: str
    caller: str
    message: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    preferred_time: Optional[str] = None
    intent: Optional[str] = None
