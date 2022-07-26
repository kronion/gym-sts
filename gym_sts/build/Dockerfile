FROM ubuntu:20.04

WORKDIR /game

RUN apt-get update &&  apt-get install -y \
    alsa-utils \
    htop `: # useful diagnostic tool` \
    libopenal1 \
    openjdk-8-jre `: # java` \
    x11-xserver-utils \
    xvfb `: # virtual X screen` \
    scrot `: # utility to take screenshots`

COPY preferences preferences

COPY info.displayconfig info.displayconfig

# Set default sound card to index 1, which is expected to be a
# loopback sound card created by the host
COPY asound.conf /etc/asound.conf

# modthespire assumes you've installed the game through steam, so we have to trick it
# into thinking nothing is amiss.
# NB: WORKDIR statements create non-existent directories recursively
WORKDIR /root/.steam/steam/steamapps
RUN touch appmanifest_646570.acf  # modthespire expects this file to be present
WORKDIR common/SlayTheSpire
RUN ln -s /game/lib/desktop-1.0.jar
WORKDIR jre/bin
RUN ln -s /etc/alternatives/java  # modthespire uses the java JRE included with the game

WORKDIR /root/.config/ModTheSpire/CommunicationMod
COPY communication_mod.config.properties config.properties

WORKDIR /root/.config/ModTheSpire/SuperFastMode
COPY superfastmode.config.properties SuperFastModeConfig.properties

WORKDIR /game
COPY pipe_to_host.sh pipe_to_host.sh

ENTRYPOINT ["xvfb-run", "-e", "/dev/stdout", "-f", "/tmp/sts.xauth", "-s", "-screen 0 1024x576x24"]
CMD ["java", "-jar", "/game/lib/ModTheSpire.jar", "--skip-intro", "--mods", "basemod,CommunicationMod,superfastmode"]
