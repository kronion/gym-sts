#!/bin/bash
# Must include the init flag so xvfb-run can use signals for IPC
docker run -it --rm -v $(pwd)/out:/out --device /dev/snd --init sts "${@}"
