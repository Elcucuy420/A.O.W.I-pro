import os
import json
from typing import Optional
from core.intents import IntentRouter
from core.memory import Memory
from integrations.google_calendar import GoogleCalendarIntegration
from integrations.gmail_handler import GmailHandler
from integrations.tripletex_invoice import TripletexInvoiceIntegration
from integrations.vipps_api import VippsIntegration


class AIReceptionistAgent:
    def __init__(self, config_dir: str = "config") -> None:
        # Load configuration files
        business_path = os.path.join(config_dir, "business.json")
        integrations_path = os.path.join(config_dir, "integrations.json")
        if os.path.exists(business_path):
            with open(business_path, "r", encoding="utf-8") as f:
                self.business = json.load(f)
        else:
            self.business = {}
        if os.path.exists(integrations_path):
            with open(integrations_path, "r", encoding="utf-8") as f:
                self.integrations_cfg = json.load(f)
        else:
            self.integrations_cfg = {}

        # Set up intent router and memory
        self.router = IntentRouter()
        self.memory = Memory()

        # Set up integrations
        self.calendar = GoogleCalendarIntegration(enabled=self.integrations_cfg.get("google_calendar", {}).get("enabled", False))
        self.gmail = GmailHandler(enabled=self.integrations_cfg.get("gmail", {}).get("enabled", False))
        self.invoice = TripletexInvoiceIntegration(enabled=self.integrations_cfg.get("tripletex", {}).get("enabled", False))
        self.vipps = VippsIntegration(enabled=self.integrations_cfg.get("vipps", {}).get("enabled", False))

    async def handle_message(self, message: str, session_id: Optional[str] = None) -> str:
        """Process a user message and return a reply.

        This method classifies the user intent and dispatches to the appropriate handler.
        Session history is stored in memory.
        """
        session_id = session_id or "default"
        # Remember the incoming message
        self.memory.add_message(session_id, {"role": "user", "content": message})
        intent = self.router.classify(message)
        reply: str

        if intent == "booking":
            # Attempt to create a calendar event using a placeholder time
            if self.calendar.enabled:
                try:
                    confirmation = await self.calendar.create_event("Appointment", "2025-11-02T10:00", "2025-11-02T10:30")
                    reply = f"{confirmation} A reminder will be sent to you."
                except Exception as ex:
                    reply = f"Failed to schedule: {ex}"
            else:
                reply = "Booking requested but calendar integration is disabled."
        elif intent == "price_query":
            # Search for the service in the business config and return its price
            lower = message.lower()
            reply = None
            for service in self.business.get("services", []):
                if service["name"].lower() in lower:
                    reply = f"{service['name']} costs {service['price']}."
                    break
            if reply is None:
                reply = "Could you specify which service you would like a price for?"
        else:
            reply = "I'm sorry, I didn't quite understand that. Could you rephrase?"

        # Store the reply in memory and return it
        self.memory.add_message(session_id, {"role": "assistant", "content": reply})
        return reply
