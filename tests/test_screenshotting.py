from unittest.mock import patch

import pytest

from gym_sts.exceptions import StSTimeoutError


def test_screenshot_regardless_of_animation(env, headless):
    if not headless:
        pytest.skip("Test can only run headless for now")

    filename = "test.png"
    filepath = env.output_dir / "screenshots" / filename

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

    folder = env.output_dir / "screenshots"
    folder_contents = list(folder.iterdir())
    assert len(folder_contents) == 0

    with patch.object(
        env.communicator, "_manual_command", side_effect=StSTimeoutError("testing")
    ):
        with pytest.raises(StSTimeoutError):
            env.step(1)
        folder_contents = list(folder.iterdir())
        assert len(folder_contents) == 1
        folder_contents[0].unlink()
