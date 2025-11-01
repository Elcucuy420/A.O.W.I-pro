class VippsIntegration:
    """
    Integration stub for the Vipps payment API. This class provides a simple
    interface for initiating payments through Vipps. In this placeholder
    implementation no real API calls are made.
    """

    def __init__(self, enabled: bool = False, credentials: dict | None = None) -> None:
        self.enabled = enabled
        self.credentials = credentials

    def create_payment(self, amount: float, phone_number: str, transaction_text: str | None = None) -> dict:
        """
        Initiate a payment request via Vipps. Raises a RuntimeError if disabled.

        :param amount: The amount in NOK to be charged.
        :param phone_number: The customer's phone number registered with Vipps.
        :param transaction_text: Optional description for the transaction.
        :return: A dictionary representing the created payment.
        """
        if not self.enabled:
            raise RuntimeError("Vipps integration is disabled.")
        # Real implementation would call the Vipps API here.
        return {
            "status": "created",
            "amount": amount,
            "phone_number": phone_number,
            "transaction_text": transaction_text,
            "payment_id": "VIPPS-0001",
        }
