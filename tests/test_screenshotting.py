from unittest.mock import patch

import pytest

from gym_sts.exceptions import StSTimeoutError


def test_screenshot_regardless_of_animation(env, headless):
    if not headless:
        pytest.skip("Test can only run headless for now")

    filename = "test.png"
    filepath = env.output_dir / filename

    for setting in [True, False]:
        env.set_animate(setting)

        # TODO confirm screenshot isn't black?
        assert not filepath.exists()
        env.screenshot(filename)
        assert filepath.exists()
        filepath.unlink()

        # Animation settings are restored after screenshot
        assert env.animate == setting


def test_screenshot_on_step_error(env, headless):
    if not headless:
        pytest.skip("Test can only run headless for now")

    assert not (env.output_dir / "error.png").exists()

    with patch.object(
        env.communicator, "_manual_command", side_effect=StSTimeoutError("testing")
    ):
        with pytest.raises(StSTimeoutError):
            env.step(1)
        assert (env.output_dir / "error.png").exists()
