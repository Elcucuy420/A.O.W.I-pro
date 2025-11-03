import json
from .config import ChannelConfig, EvolutionRules, Settings
from .pipeline import Autopilot

def bootstrap():
    cfg = ChannelConfig()
    evo = EvolutionRules()
    st = Settings()
    bot = Autopilot(cfg, evo, st)
    out = bot.run_once()
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    bootstrap()
