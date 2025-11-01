import os
import base64
import requests
from email.message import EmailMessage
from typing import Optional

class GmailHandler:
    """
    Integration for sending emails via Gmail's REST API.
    Requires an environment variable GMAIL_API_TOKEN containing a valid OAuth2 access token.
    """
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    async def send_email(
        self, to_email: str, subject: str, body: str, from_email: Optional[str] = None
    ) -> dict:
        """
        Send an email using Gmail API.
        :param to_email: Recipient email address.
        :param subject: Subject line for the email.
        :param body: Body text of the email.
        :param from_email: Optional sender email address.
        :return: A dictionary with status and Gmail message IDs.
        """
        if not self.enabled:
            raise RuntimeError("Gmail integration is disabled.")

        token = os.getenv("GMAIL_API_TOKEN")
        if not token:
            raise RuntimeError("GMAIL_API_TOKEN not set in environment.")

        # Construct the email message
        msg = EmailMessage()
        msg["To"] = to_email
        msg["Subject"] = subject
        if from_email:
            msg["From"] = from_email
        msg.set_content(body)

        # Encode the message to base64url as required by Gmail API
        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        data = {"raw": encoded_message}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        # Send the message
        url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"Gmail API call failed: {response.status_code} {response.text}"
            )

        resp_json = response.json()
        return {
            "status": "sent",
            "id": resp_json.get("id"),
            "threadId": resp_json.get("threadId"),
        }
