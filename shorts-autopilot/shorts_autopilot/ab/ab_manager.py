import random
from typing import List, Dict
from ..text.hook_variants import variants as hook_variants

class ABManager:
    def __init__(self, k:int=2):
        self.k = k
    def make_variants(self, topic:str) -> List[str]:
        return hook_variants(topic, k=self.k)
    def pick_winner(self, candidates: List[Dict]) -> Dict:
        best=None; best_score=-1.0
        for c in candidates:
            m=c.get('metrics',{})
            ctr=float(m.get('ctr',0.05))/0.08
            ret=float(m.get('retention',0.35))/0.45
            score=0.4*ctr+0.6*ret
            if score>best_score:
                best=c; best_score=score
        return best or (candidates[0] if candidates else {})
