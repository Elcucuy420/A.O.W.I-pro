import os
SESSION = os.getenv('TIKTOK_SESSION_ID')

def upload_short_tiktok(path: str, title: str, tags=None):
    if not SESSION:
        return {'ok': False, 'reason': 'missing TIKTOK_SESSION_ID'}
    return {'ok': False, 'reason': 'uploader not implemented'}
