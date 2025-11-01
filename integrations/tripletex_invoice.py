class TripletexInvoiceIntegration:
    """
    Integration stub for generating invoices via the Tripletex API. This
    placeholder defines the basic methods expected from an invoicing system
    without implementing the actual API calls.
    """

    def __init__(self, enabled: bool = False, credentials: dict | None = None) -> None:
        self.enabled = enabled
        self.credentials = credentials

    def create_invoice(self, customer: dict, items: list[dict]) -> dict:
        """
        Create an invoice for the given customer with a list of items. Each item
        dict can include fields like description, quantity, and unit price. If
        the integration is disabled, a RuntimeError will be raised.

        :param customer: Information about the customer (name, contact, etc.)
        :param items: A list of invoice line items
        :return: A dictionary representing the created invoice
        """
        if not self.enabled:
            raise RuntimeError("Tripletex integration is disabled.")
        # Real implementation would call the Tripletex API to create an invoice.
        return {
            "status": "success",
            "customer": customer,
            "items": items,
            "invoice_number": "TEMP-12345",
        }
