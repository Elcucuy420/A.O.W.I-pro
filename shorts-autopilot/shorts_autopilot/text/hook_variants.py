import random
TEMPLATES=["Stop scrolling: {topic} in 30s","3 {topic} you didn't expect","Nobody told you this about {topic}","{topic} that feels illegal to know"]

def variants(topic: str, k: int=3):
    topic=topic.strip().rstrip('.')
    picks=random.sample(TEMPLATES, k=min(k,len(TEMPLATES)))
    return [p.format(topic=topic) for p in picks]
