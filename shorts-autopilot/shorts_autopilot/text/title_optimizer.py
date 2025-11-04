import re
HOOK_PATTERNS=["3 {topic} you didn't expect","{topic} that feel illegal to know","Stop scrolling: {topic} in 30s"]
def best_title(topic: str):
    t = topic.strip().rstrip('.')
    return HOOK_PATTERNS[0].format(topic=t)
