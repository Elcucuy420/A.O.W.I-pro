import os, httpx
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY','')
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

def search_youtube_trends(query: str, max_results: int = 10):
    if not YOUTUBE_API_KEY:
        return []
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'relevanceLanguage': 'en',
        'order': 'viewCount',
        'key': YOUTUBE_API_KEY
    }
    with httpx.Client(timeout=20) as client:
        r = client.get(YOUTUBE_SEARCH_URL, params=params)
        r.raise_for_status()
        data = r.json()
        ideas = []
        for item in data.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            ideas.append({'source':'youtube','video_id':video_id,'title':title})
        return ideas
