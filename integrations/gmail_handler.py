class GmailHandler:
    """
    Integration stub for sending and handling emails via Gmail. In a full
    implementation this class would authenticate with the Gmail API and
    provide methods for sending, receiving, and parsing emails. Currently
    it serves as a placeholder.
    """

    def __init__(self, enabled: bool = False, credentials: dict | None = None) -> None:
        self.enabled = enabled
        self.credentials = credentials

    def send_email(self, to_email: str, subject: str, body: str) -> dict:
        """
        Send an email via Gmail. Raises a RuntimeError if the integration is
        disabled. Returns a placeholder response.

        :param to_email: Recipient email address.
        :param subject: Subject line for the email.
        :param body: Body text of the email.
        :return: A dictionary representing the response from the email send.
        """
        if not self.enabled:
            raise RuntimeError("Gmail integration is disabled.")
        # Real implementation would use the Gmail API here.
        return {
            "status": "sent",
            "to": to_email,
            "subject": subject,
            "body": body,
        }
