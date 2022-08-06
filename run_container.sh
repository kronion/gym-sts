#!/bin/bash
# Must include the init flag so xvfb-run can use signals for IPC
docker run -it --rm --device /dev/snd --init sts "${@}"
