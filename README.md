gym-sts
===

An OpenAI Gym env for Slay the Spire.

All installation commands are expected to be run as root.

# Installation

1. Install the package along with its dependencies:
```
pip install -e .

# Alternatively, you can use poetry
poetry install
```

2. Pull in required jar files. Directory structure should look like this:
```
gym-sts/
  gym_sts/
    ...
  lib/
    desktop-1.0.jar
    ModTheSpire.jar
  mods/
    BaseMod.jar
    CommunicationMod.jar
```

# Build

To build the Docker container:
```
from gym_sts.envs.base import SlayTheSpireGymEnv
SlayTheSpireGymEnv.build_image()
```

# Setup

```
# On the host, make sure a loopback sound card has been created
modprobe snd-aloop  # TODO can an index be assigned?
```

# Run

## Run the game headless in a Docker container (preferred)

The Python script will start the container. You can communicate with the game using
CommunicationMod commands via stdin.

```
python3 -m gym_sts.runner [lib_dir] [mod_dir] [out_dir] --headless
```

## Run the game directly on the host

The Python script will start the game as a subprocess. This allows for easy observation
of gameplay. You can communicate with the game using CommunicationMod commands via
stdin.


```
python3 -m gym_sts.runner [lib_dir] [mod_dir] [out_dir]
```
