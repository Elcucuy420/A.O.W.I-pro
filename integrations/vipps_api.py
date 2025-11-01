import os
import uuid
import requests
from typing import Optional

class VippsIntegration:
    """
    Integration for creating payment requests via the Vipps ePayment API.
    Requires environment variables VIPPS_API_TOKEN, VIPPS_SUBSCRIPTION_KEY,
    VIPPS_MERCHANT_SERIAL and optionally VIPPS_RETURN_URL.
    """

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    async def create_payment(
        self,
        amount: float,
        phone_number: str,
        transaction_text: str,
        return_url: Optional[str] = None,
    ) -> dict:
        """
        Initiate a payment request via Vipps.

        :param amount: The amount in NOK to be charged.
        :param phone_number: The customer's phone number (international format).
        :param transaction_text: Description shown to the customer.
        :param return_url: Optional URL to redirect the user after payment completion.
        :return: A dictionary with status and payment identifiers.
        """
        if not self.enabled:
            raise RuntimeError("Vipps integration is disabled.")

        api_token = os.getenv("VIPPS_API_TOKEN")
        subscription_key = os.getenv("VIPPS_SUBSCRIPTION_KEY")
        merchant_serial = os.getenv("VIPPS_MERCHANT_SERIAL")
        if not api_token or not subscription_key or not merchant_serial:
            raise RuntimeError(
                "VIPPS_API_TOKEN, VIPPS_SUBSCRIPTION_KEY, and VIPPS_MERCHANT_SERIAL must be set."
            )

        # Vipps expects amounts in the smallest currency unit (øre), multiply NOK by 100
        amount_in_ore = int(round(amount * 100))
        payment_id = str(uuid.uuid4())
        payload = {
            "amount": {"currency": "NOK", "value": amount_in_ore},
            "customer": {"phoneNumber": phone_number},
            "paymentMethod": {"type": "WALLET"},
            "reference": payment_id,
            "paymentDescription": transaction_text,
            "returnUrl": return_url or os.getenv("VIPPS_RETURN_URL", "https://example.com/thanks"),
            "userFlow": "WEB_REDIRECT",
        }

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Merchant-Serial-Number": merchant_serial,
            "Idempotency-Key": payment_id,
            "Content-Type": "application/json",
        }

        url = "https://api.vipps.no/epayment/v1/payments"
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"Vipps API call failed: {response.status_code} {response.text}"
            )

        resp_json = response.json()
        return {
            "status": "created",
            "paymentId": resp_json.get("paymentId"),
            "redirectUrl": resp_json.get("redirectUrl"),
        }
