from pydantic import BaseModel
from typing import List, Optional

class ChannelConfig(BaseModel):
    name: str
    target_platforms: List[str] = ['youtube','tiktok']
    language: str = 'en'
    niche_goal: str = 'evergreen-psychology'
    rpm_hint: float = 4.0

class EvolutionRules(BaseModel):
    ctr_target: float = 0.08
    retention_target: float = 0.45
    rpm_min: float = 2.0
    max_daily_pivots: int = 1

class Settings(BaseModel):
    mongo_uri: Optional[str] = None
    openai_key: Optional[str] = None
    elevenlabs_key: Optional[str] = None
    youtube_key: Optional[str] = None
    tiktok_session: Optional[str] = None

