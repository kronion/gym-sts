import pytest

from gym_sts.envs.base import SlayTheSpireGymEnv
from gym_sts.envs.single_combat import SingleCombatSTSEnv


def pytest_addoption(parser):
    parser.addoption("--lib-dir", default="lib", help="Location of the lib directory")
    parser.addoption(
        "--mods-dir", default="mods", help="Location of the mods directory"
    )
    parser.addoption(
        "--headless", action="store_true", help="If provided, run without a visible UI"
    )


@pytest.fixture
def headless(request):
    return request.config.getoption("headless")


# Because starting the game is time-consuming, we scope this fixture to the entire
# test session, i.e. the same game is used across all tests. This means each test
# must call `env.reset()` in order to ensure isolation from previous tests.
@pytest.fixture(scope="session")
def env(request):
    lib_dir = request.config.getoption("lib_dir")
    mods_dir = request.config.getoption("mods_dir")
    headless = request.config.getoption("headless")

    env = SlayTheSpireGymEnv(lib_dir, mods_dir, headless=headless)
    yield env

    env.close()


@pytest.fixture(scope="session")
def single_combat_env(request):
    lib_dir = request.config.getoption("lib_dir")
    mods_dir = request.config.getoption("mods_dir")
    headless = request.config.getoption("headless")

    env = SingleCombatSTSEnv(lib_dir, mods_dir, headless=headless)
    yield env

    env.close()
