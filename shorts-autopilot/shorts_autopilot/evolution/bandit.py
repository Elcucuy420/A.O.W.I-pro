class Arm:
    def __init__(self, name):
        self.name=name; self.success=1; self.fail=1
    def update(self, reward: float):
        if reward>0.5: self.success+=1
        else: self.fail+=1
    def sample(self):
        import random
        return random.betavariate(self.success, self.fail)

class Bandit:
    def __init__(self, arms):
        self.arms = {a:Arm(a) for a in arms}
    def pick(self):
        return max(self.arms.values(), key=lambda a:a.sample()).name
    def learn(self, arm_name, reward):
        self.arms[arm_name].update(reward)
