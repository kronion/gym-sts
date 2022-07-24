FROM ubuntu:20.04

WORKDIR /game

COPY lib lib

RUN apt-get update &&  apt-get install -y \
    alsa-utils \
    htop \
    libopenal1 \
    openjdk-8-jre \
    xvfb

ENTRYPOINT ["/bin/bash"]
