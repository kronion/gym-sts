# run with ipython -i gym_sts/env_reply.py

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.observations import Observation

env = SlayTheSpireGymEnv("lib", "mods", "out", headless=True)
obs = env.reset()
assert isinstance(obs, Observation)
print(obs.state)
