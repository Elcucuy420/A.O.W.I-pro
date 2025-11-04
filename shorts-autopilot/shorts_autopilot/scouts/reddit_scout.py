import httpx
BASE = 'https://www.reddit.com/r/{sub}/hot.json'
HEADERS = {'User-Agent':'shorts-autopilot/0.1'}

def fetch_hot(sub: str, limit: int = 10):
    url = BASE.format(sub=sub)
    with httpx.Client(timeout=20, headers=HEADERS) as c:
        r = c.get(url, params={'limit':limit})
        r.raise_for_status()
        data = r.json()
        ideas=[]
        for child in data.get('data',{}).get('children',[]):
            d = child.get('data',{})
            title = d.get('title')
            if title:
                ideas.append({'source':'reddit','sub':sub,'title':title})
        return ideas
