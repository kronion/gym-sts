from unittest.mock import patch


def test_reboot_occurs_every_reset(env):
    env.reboot_frequency = 1

    with patch.object(env, "_end_game") as mock_end_game:
        env.reset()
        env.reset()
        env.reset()

    mock_end_game.assert_not_called()
