# run with ipython -i gym_sts/env_reply.py

from gym_sts.envs.base import SlayTheSpireGymEnv
env = SlayTheSpireGymEnv("out", headless=True)
obs = env.reset()
print(obs._state)
