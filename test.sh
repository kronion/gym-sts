#!/bin/bash
INPUT="/out/stsai_input"
OUTPUT="/out/stsai_output"

function cleanup() {
    kill $BG_PID
}

trap cleanup EXIT

cat $INPUT &
BG_PID=$!
cat > $OUTPUT
