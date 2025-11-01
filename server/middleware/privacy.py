import re
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class PrivacyMiddleware(BaseHTTPMiddleware):
    """Middleware that redacts sensitive information like emails and phone numbers from JSON responses."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # Patterns to detect emails and phone numbers
        self.email_regex = re.compile(r"[\w\.-]+@[\w\.-]+\.[\w-]+")
        # Simplistic phone detection: sequences of 6-15 digits that may start with +
        self.phone_regex = re.compile(r"\+?\d{6,15}")

    async def dispatch(self, request: Request, call_next):
        # Process the request and get the response from downstream
        response: Response = await call_next(request)

        # Only process JSON responses
        if response.media_type == "application/json":
            # Read the response body into memory (it may be streamed)
            body_bytes = b""
            async for chunk in response.body_iterator:
                body_bytes += chunk

            # Decode to text and apply redactions
            content_str = body_bytes.decode("utf-8")
            content_str = self.email_regex.sub("[REDACTED]", content_str)
            content_str = self.phone_regex.sub("[REDACTED]", content_str)

            # Create a new response with the redacted content
            return Response(
                content=content_str,
                status_code=response.status_code,
                media_type=response.media_type,
                headers=dict(response.headers),
            )

        # If not JSON, return the original response unmodified
        return response
