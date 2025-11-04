import os
from typing import Optional, Dict

# Placeholder for YouTube Analytics API integration.
# When creds are provided, fetch CTR, avgViewDuration, views, subsGained by videoId.
# Return a normalized reward in [0,1] for bandit training.

HAS_OAUTH = all([
    os.getenv('YOUTUBE_CLIENT_ID'),
    os.getenv('YOUTUBE_CLIENT_SECRET'),
    os.getenv('YOUTUBE_REFRESH_TOKEN')
])

# Simple reward shaping with safe defaults if analytics not available.
def reward_from_metrics(metrics: Optional[Dict]) -> float:
    if not metrics:
        return 0.55  # neutral default to keep exploring
    ctr = float(metrics.get('ctr', 0.05))   # 5%
    ret = float(metrics.get('retention', 0.35)) # 35%
    rpm = float(metrics.get('rpm', 3.0))    # $3
    # Weighted blend → clamp 0..1
    r = 0.5*min(ctr/0.08, 1.2) + 0.4*min(ret/0.45, 1.2) + 0.1*min(rpm/5.0, 1.2)
    return max(0.0, min(r, 1.0))
