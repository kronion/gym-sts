gym-sts
===

An OpenAI Gym env for Slay the Spire.

# Installation

TODO

# Usage

To build the Docker container:
```
docker build -t sts .
```

To run the Docker container:
```
# On the host, make sure a loopback sound card has been created
modprobe snd-aloop  # TODO can an index be assigned?

# Then use the convenience script to boot the container.
# By default, the game will start with the required mods, but you
# can also specify your own command to run, e.g. /bin/bash
./run_container.sh [optional-command]
```
