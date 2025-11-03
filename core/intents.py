class IntentRouter:
    """
    Simple intent router for the AI receptionist. This router uses a basic keyword
    approach to map incoming messages to high-level intents such as greeting,
    booking, inquiries about prices or opening hours, and falls back to
    "unknown" if no keywords are matched. This is a placeholder and should be
    replaced with a more robust NLP-based intent classifier in production.
    """

    def __init__(self) -> None:
        # Define simple keyword lists for each intent.
        self.intents = {
            "greeting": ["hello", "hi", "hei", "hallo"],
            "booking": ["book", "schedule", "avtale", "time"],
            "price": ["price", "cost", "pris", "koster"],
            "hours": ["hours", "open", "\u00e5pningstider", "when"],
        }

    def classify(self, message: str) -> str:
        """
        Very basic keyword-based classifier returning an intent name based on
        whether any of the keywords appear in the message. If no keywords
        match, it returns "unknown".

        :param message: The user message to classify.
        :return: The intent name.
        """
        message_lower = message.lower()
        for intent, keywords in self.intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        return "unknown"
