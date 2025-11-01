class Memory:
    """
    Simple in-memory storage for user sessions and conversation context. In a
    production environment, this could be replaced with a persistent database
    or stateful cache. For now, it tracks user sessions in a Python dict.
    """

    def __init__(self) -> None:
        # Dictionary mapping user_id to their session data dictionary
        self.sessions: dict[str, dict] = {}

    def get_session(self, user_id: str) -> dict:
        """
        Retrieve the session data for a given user. Returns an empty dict if
        no session exists.

        :param user_id: Unique identifier for the user (e.g., phone number or email).
        :return: The session data dictionary.
        """
        return self.sessions.get(user_id, {})

    def update_session(self, user_id: str, key: str, value) -> None:
        """
        Update a key-value pair in the user's session. If the session does not
        exist, it will be created.

        :param user_id: Unique identifier for the user.
        :param key: The session attribute to update.
        :param value: The value to store under the specified key.
        """
        session = self.sessions.setdefault(user_id, {})
        session[key] = value

    def clear_session(self, user_id: str) -> None:
        """
        Remove the user's session entirely. Useful when a conversation is
        completed or should start fresh.

        :param user_id: Unique identifier for the user.
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
