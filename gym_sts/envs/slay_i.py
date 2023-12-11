from gym_sts.spaces.actions import ACTIONS

from .action_validation import validate
from .base import SlayTheSpireGymEnv



class SlayIEnv(SlayTheSpireGymEnv):
    def step(self, action_id: int) -> Tuple[dict, float, bool, bool, dict]:
        prev_obs = self.observation_cache.get()
        assert prev_obs is not None  # should have been set by reset()

        action = ACTIONS[action_id]
        is_valid = validate(action, prev_obs)

        try:
            obs = self.communicator._manual_command(action.to_command())
        except Exception as e:
            logging.error(e)
            print(prev_obs)
            print(action_id)
            now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            try:
                self.screenshot(f"error_{now}.png")
            except NotImplementedError:
                pass

            if not self.reboot_on_error:
                raise e

            # Reboot and return done=True to trigger a reset
            self.reboot()
            obs = prev_obs
            info = {
                "observation": obs,
                "had_error": obs.has_error,
                "reboot_error": e,
            }
            return obs.serialize(), 0.0, True, False, info

        if obs.has_error == is_valid:
            # indicates a mismatch in our action validity checking
            logging.error(
                "Action was %svalid, but obs %s an error.",
                "" if is_valid else "not ",
                "had" if obs.has_error else "did not have",
            )

        had_error = obs.has_error
        if had_error:
            reward = -1.0
            # Maybe check that the new obs is the same as the old one, modulo
            # the error field?
            obs = prev_obs
        else:
            success = False
            for _ in range(10):
                if len(obs.valid_actions) == 0:
                    # this can indicate instability
                    time.sleep(1)
                    obs = self.observe()
                else:
                    success = True
                    break
            if not success:
                print(obs.state)
                raise exceptions.StSError("No valid actions.")

            if obs.screen_type == ScreenType.CARD_REWARD:
                obs = self.slay_i_predict(obs)

            # Send observation to state logger
            if self.log_states:
                self.state_logger.log(action, obs)

            reward = self.value_fn(obs) - self.value_fn(prev_obs)
            self.observation_cache.append(obs)

        info = {
            "observation": obs,
            "had_error": had_error,
        }

        return obs.serialize(), reward, obs.game_over, False, info

    def slay_i_predict(self, obs: Observation) -> Observation:
        # TODO create the input that the model needs, using the Observation object and any other necessary data
        # (like the elites and bosses in the act)
        
        # Open question: Slay-I usually computes at the start of combat, but we're trying to compute right when we
        # see the card reward. Is this invalid for some reason? Or maybe it's just slow?
