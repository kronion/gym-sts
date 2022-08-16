#!/bin/bash
INPUT="out/stsai_input"
OUTPUT="out/stsai_output"

function cleanup() {
    kill $BG_PID
}

trap cleanup EXIT

cat $INPUT &
BG_PID=$!

# Sleep to allow time for the background process to start
sleep 0.2

cat > $OUTPUT
