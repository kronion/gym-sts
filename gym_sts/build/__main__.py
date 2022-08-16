import sys
from pathlib import Path

import sh


def build():
    dockerfile = f"{Path(__file__).parent.absolute()}/Dockerfile"

    sh.docker.build(
        "-t", "sts",
        "--file",
        dockerfile,
        ".",  # This must be the root of the repo
        _out=sys.stdout,
        _err=sys.stderr,
    )



if __name__ == "__main__":
    build()
