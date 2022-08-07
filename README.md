gym-sts
===

An OpenAI Gym env for Slay the Spire.

All installation commands are expected to be run as root.

# Installation

TODO

# Build

To build the Docker container:
```
docker build -t sts .
```

# Setup

```
# On the host, make sure a loopback sound card has been created
modprobe snd-aloop  # TODO can an index be assigned?
```

# Run

## Python script outside container (preferred)

This lets the Python script start the container.

```
python3 gym_sts/runner.py
```

## Python script inside container

This lets the container start the Python script.

```
# Use the convenience script to boot the container.
# By default, the game will start with the required mods, but you
# can also specify your own command to run, e.g. /bin/bash
./run_container.sh [optional-command]
```
