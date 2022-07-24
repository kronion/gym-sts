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

docker run -it --rm --device /dev/snd sts

# Once you're inside the container, run:
java -jar lib/desktop-1.0.jar
```
