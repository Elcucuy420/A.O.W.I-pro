import os
import requests
from typing import Optional

class GoogleCalendarIntegration:
    """
    Real integration with the Google Calendar API.
    This class can create events on a connected Google Calendar when enabled.
    """

    def __init__(self, enabled: bool = False, calendar_id: str = "primary") -> None:
        self.enabled = enabled
        self.calendar_id = calendar_id

    async def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        timezone: str = "Europe/Oslo",
        description: str = "",
        attendee_email: Optional[str] = None,
    ) -> str:
        """
        Create an event on Google Calendar. This requires a valid OAuth 2 access token
        stored in the `GOOGLE_CALENDAR_API_TOKEN` environment variable.

        :param summary: Title of the event.
        :param start_time: ISO 8601 start date/time (e.g., "2025-11-02T10:00:00").
        :param end_time: ISO 8601 end date/time.
        :param timezone: IANA time zone (e.g., "Europe/Oslo").
        :param description: Optional event description.
        :param attendee_email: Optional attendee e m‑mail to add to the event.
        :return: A human‭friendly confirmation string.
        """
        if not self.enabled:
            raise RuntimeError("Google Calendar integration is disabled.")

        access_token = os.getenv("GOOGLE_CALENDAR_API_TOKEN")
        if not access_token:
            raise RuntimeError(
                "GOOGLE_CALENDAR_API_TOKEN environment variable is not set."
            )

        url = f"https://www.googleapis.com/calendar/v3/calendars/{self.calendar_id}/events"
        event_body: dict = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        }
        if attendee_email:
            event_body["attendees"] = [{"email": attendee_email}]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=event_body)
        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Google Calendar API error: {response.status_code} - {response.text}"
            )

        data = response.json()
        event_link = data.get("htmlLink")
        return (
            f"Event created successfully"
            + (f" – see {event_link}" if event_link else "")
            + "."
        )
