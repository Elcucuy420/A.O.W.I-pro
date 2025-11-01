import os
import requests
from typing import List, Dict, Optional

class TripletexInvoiceIntegration:
    """
    Integration for generating invoices via the Tripletex API.
    Requires an environment variable TRIPLETEX_API_TOKEN containing a valid API token.
    """

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    async def create_invoice(
        self,
        customer: Dict[str, any],
        items: List[Dict[str, any]],
        due_date: Optional[str] = None,
    ) -> dict:
        """
        Create an invoice for the given customer with a list of items.

        :param customer: Information about the customer (e.g., name, email, id).
        :param items: List of invoice line items containing description, quantity, unit price, etc.
        :param due_date: Optional due date for the invoice in ISO format (YYYY-MM-DD).
        :return: A dictionary with status and invoice identifiers.
        """
        if not self.enabled:
            raise RuntimeError("Tripletex integration is disabled.")

        token = os.getenv("TRIPLETEX_API_TOKEN")
        if not token:
            raise RuntimeError("TRIPLETEX_API_TOKEN not set in environment.")

        # Build the invoice payload according to Tripletex API schema
        invoice_payload = {
            "customer": customer,
            "invoiceLines": items,
        }
        if due_date:
            invoice_payload["dueDate"] = due_date

        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }
        # Endpoint for creating invoices; adjust path if API version differs
        url = "https://tripletex.no/v2/invoice"
        response = requests.post(url, headers=headers, json=invoice_payload, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"Tripletex API call failed: {response.status_code} {response.text}"
            )

        resp_json = response.json()
        return {
            "status": "created",
            "invoiceId": resp_json.get("invoiceNumber") or resp_json.get("id"),
            "url": resp_json.get("url"),
        }
