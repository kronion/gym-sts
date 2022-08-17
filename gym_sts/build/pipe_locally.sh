#!/bin/bash

# Pipe CommunicationMod IO to FIFOs provided by the host

INPUT=$1
OUTPUT=$2

function cleanup() {
    kill $BG_PID
}

trap cleanup EXIT

cat $INPUT &
BG_PID=$!

# Sleep to allow time for the background process to start
sleep 0.2

cat > $OUTPUT
