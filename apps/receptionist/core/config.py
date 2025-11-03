from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Service
    ENV: str = 'dev'
    ALLOWED_ORIGINS: str = '*'
    ENABLE_RATE_LIMIT: bool = True

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = 'gpt-4o-mini'

    # Twilio
    TWILIO_AUTH_TOKEN: Optional[str] = None
    VERIFY_TWILIO_SIGNATURE: bool = False

    # Booking webhooks
    CALCOM_WEBHOOK: Optional[AnyUrl] = None
    GOOGLE_CAL_WEBHOOK: Optional[AnyUrl] = None

    # Persistence
    LEADS_DB_URL: str = 'sqlite+aiosqlite:///./leads.db'

settings = Settings()
