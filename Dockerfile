FROM ubuntu:20.04

WORKDIR /game

COPY lib lib

RUN apt-get update &&  apt-get install -y \
    alsa-utils \
    htop \
    libopenal1 \
    openjdk-8-jre \
    x11-xserver-utils \
    xvfb

# Set default sound card to index 1, which is expected to be a
# loopback sound card created by the host
COPY asound.conf /etc/asound.conf

ENTRYPOINT xvfb-run -s '-screen 0 1024x768x24' /bin/bash
