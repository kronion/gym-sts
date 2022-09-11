from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()

JAVA_INSTALL = "/usr/bin/java"
MTS_JAR = "ModTheSpire.jar"
EXTRA_ARGS = ["--skip-launcher", "--skip-intro", "--mods", "basemod,CommunicationMod"]

DOCKER_IMAGE_TAG = "sts"

EVENTS_JSON_PATH = "data/events.json"
