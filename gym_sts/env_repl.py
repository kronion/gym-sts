# run with ipython -i gym_sts/env_repl.py

from gym_sts.envs.base import SlayTheSpireGymEnv

SlayTheSpireGymEnv.build_image()
env = SlayTheSpireGymEnv("lib", "mods", "out", headless=True)
obs = env.reset()
