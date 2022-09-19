gym-sts
===

An OpenAI Gym env for Slay the Spire.

All installation commands are expected to be run as root.

# Requirements

- Java JDK 8
- Docker
- A copy of Slay the Spire, particularly its `desktop-1.0.jar` file.
- The JAR files for several mods:
  - ModTheSpire
  - BaseMod
  - CommunicationMod
  - SuperFastMode

This package has been tested with Python 3.9, but more recent Pythons may also work
as long as you can build dependencies (there may not be prebuilt wheels).

# Installation

IMPORTANT: These instructions assume you're a developer of this library, not that you're
trying to add this library as a dependency for another project.

1. Install the package along with its dependencies:

```zsh
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
    SuperFastMode.jar
```

# Build

To build the Docker container:

```python
from gym_sts.envs.base import SlayTheSpireGymEnv

SlayTheSpireGymEnv.build_image()
```

# Setup

```zsh
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

# Developer guide

1. After cloning the project, use [poetry](python-poetry.org/) to install dependencies
in a virtual environment:

```zsh
poetry install

# Enter the venv in a subshell
poetry shell
```

This project uses [pre-commit](https://pre-commit.com/) to configure various
linters/fixers. Make sure you've installed the pre-commit hook:

```zsh
# Confirm pre-commit is installed
pre-commit -V

# Install the hook
pre-commit install

# Optionally run the linters manually
pre-commit run --all-files
```
