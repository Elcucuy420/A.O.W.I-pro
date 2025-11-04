import os
from textwrap import shorten
USE_OPENAI = bool(os.getenv('OPENAI_API_KEY'))

def write(topic: str, title: str):
    # Simple, fast writer; upgrade to OpenAI if key exists
    hook=title
    beats=[f'1) {topic} fact you can apply today', f'2) Quick take that surprises people', '3) End with curiosity gap']
    cta='Follow for more.'
    return {'hook':hook,'body':beats,'cta':cta}
