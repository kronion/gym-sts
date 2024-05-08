import random
from collections.abc import Iterable

from gym_sts.spaces.constants.base import ScreenType

from .base import SlayTheSpireGymEnv


class STSScreenLimitedEnv(SlayTheSpireGymEnv):
    def __init__(
        self, *args, allowed_screen_types: Iterable[ScreenType] | None = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.allowed_screen_types = allowed_screen_types

    def reset(self, *args, **kwargs) -> tuple[dict, dict]:
        serialized_obs, info = super().reset(*args, **kwargs)

        obs = info["observation"]
        screen_type = obs.screen_type

        if self.allowed_screen_types is not None:
            attempt = 0
            ATTEMPT_LIMIT = 100

            while screen_type not in self.allowed_screen_types:
                if attempt >= ATTEMPT_LIMIT:
                    raise Exception("Couldn't reach an allowed screen type")

                # Randomly choose an action
                valid_actions = self.valid_actions()
                action = random.choice(valid_actions)

                serialized_obs, _, terminated, truncated, info = super().step(
                    action._id
                )

                if terminated or truncated:
                    serialized_obs, info = super().reset(*args, **kwargs)
                    attempt = 0
                else:
                    attempt += 1

                obs = info["observation"]
                screen_type = obs.screen_type
                print(screen_type)

        return serialized_obs, info

    def step(self, action_id: int) -> tuple[dict, float, bool, bool, dict]:
        serialized_obs, reward, terminated, truncated, info = super().step(action_id)

        if terminated or truncated:
            return serialized_obs, reward, terminated, truncated, info

        obs = info["observation"]
        screen_type = obs.screen_type

        if self.allowed_screen_types is not None:
            attempt = 0
            ATTEMPT_LIMIT = 100

            while screen_type not in self.allowed_screen_types:
                if attempt >= ATTEMPT_LIMIT:
                    raise Exception("Couldn't reach an allowed screen type")

                # Randomly choose an action
                valid_actions = self.valid_actions()
                action = random.choice(valid_actions)

                serialized_obs, reward, terminated, truncated, info = super().step(
                    action._id
                )

                if terminated or truncated:
                    break

                obs = info["observation"]
                screen_type = obs.screen_type
                attempt += 1

        return serialized_obs, reward, terminated, truncated, info
