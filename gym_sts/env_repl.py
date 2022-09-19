# run with ipython -i gym_sts/env_repl.py

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.spaces.observations import Observation

SlayTheSpireGymEnv.build_image()
env = SlayTheSpireGymEnv("lib", "mods", "out", headless=True)
obs = env.reset()
assert isinstance(obs, Observation)
print(obs.state)
