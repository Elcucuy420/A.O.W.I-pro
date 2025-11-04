import os
from typing import Optional, Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES=['https://www.googleapis.com/auth/yt-analytics.readonly']

def _creds():
    if not (os.getenv('YOUTUBE_CLIENT_ID') and os.getenv('YOUTUBE_CLIENT_SECRET') and os.getenv('YOUTUBE_REFRESH_TOKEN')):
        return None
    return Credentials(
        None, refresh_token=os.getenv('YOUTUBE_REFRESH_TOKEN'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=os.getenv('YOUTUBE_CLIENT_ID'),
        client_secret=os.getenv('YOUTUBE_CLIENT_SECRET'),
        scopes=SCOPES
    )

def fetch_video_metrics(video_id: str) -> Optional[Dict]:
    creds=_creds()
    if creds is None: return None
    ya = build('youtubeAnalytics','v2',credentials=creds)
    # Last 14 days for stability
    req = ya.reports().query(
        ids='channel==MINE',
        startDate='2024-01-01', endDate='2099-01-01',
        dimensions='video', filters=f'video=={video_id}',
        metrics='views,impressions,averageViewDuration,impressionsCtr,subscribersGained'
    )
    resp = req.execute()
    rows = resp.get('rows',[])
    if not rows: return None
    # video,views,impressions,avd,ctr,subs
    _, views, imps, avd, ctr, subs = rows[0]
    ctr = float(ctr) if ctr is not None else 0.05
    ret = float(avd)/30.0 if avd else 0.35
    return {'ctr': max(0.0,min(ctr,1.0)), 'retention': max(0.0,min(ret,1.0)), 'rpm': 3.0, 'views':views, 'impressions':imps, 'subs':subs}
