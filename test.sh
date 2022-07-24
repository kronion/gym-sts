#!/bin/bash
INPUT="/tmp/stsai_input"
OUTPUT="/tmp/stsai_output"

function cleanup() {
    kill $BG_PID
}

trap cleanup EXIT

cat $INPUT &
BG_PID=$!
cat > $OUTPUT
