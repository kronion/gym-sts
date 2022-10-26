from unittest.mock import patch


def test_reboot_occurs_every_reset(env):
    env.reset_count = 0
    env.reboot_frequency = 1

    with patch.object(env, "_end_game") as mock_end_game:
        env.reset()
        env.reset()
        env.reset()

    mock_end_game.assert_not_called()


def test_reboot_occurs_only_once(env):
    env.reset_count = 0
    env.reboot_frequency = 0
    env.reset()

    with patch.object(env, "reboot") as mock_reboot:
        env.reset()
        env.reset()
        mock_reboot.assert_not_called()


def test_reboot_occurs_every_other_time(env):
    env.reset_count = 0
    env.reboot_frequency = 2

    with patch.object(env, "_end_game", side_effect=env._end_game) as mock_end_game:
        with patch.object(env, "reboot", side_effect=env.reboot) as mock_reboot:
            for i in range(6):
                env.reset()
                if i % 2 == 0:
                    mock_reboot.assert_called_once()
                else:
                    mock_end_game.assert_called_once()

                mock_reboot.reset_mock()
                mock_end_game.reset_mock()


def test_force_reboot(env):
    env.reset_count = 0
    env.reboot_frequency = 0
    env.reset()

    with patch.object(env, "reboot", side_effect=env.reboot) as mock_reboot:
        env.reset()
        mock_reboot.assert_not_called()

        env.reset(options={"reboot": True})
        mock_reboot.assert_called_once()
