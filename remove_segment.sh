#!/bin/bash

# Check if correct number of arguments provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 <video_file> <start_time> <end_time>"
    echo "Removes the segment between <start_time> and <end_time> from the video."
    echo "Example: $0 video.mp4 10 30"
    echo "Example: $0 video.mp4 1:30 2:45"
    exit 1
fi

INPUT_VIDEO="$1"
START_TIME="$2"
END_TIME="$3"

if [ ! -f "$INPUT_VIDEO" ]; then
    echo "Error: Video file '$INPUT_VIDEO' not found"
    exit 1
fi

DIR=$(dirname "$INPUT_VIDEO")
FILENAME=$(basename "$INPUT_VIDEO")
NAME="${FILENAME%.*}"
EXT="${FILENAME##*.}"

OUTPUT_VIDEO="${DIR}/${NAME}_edited.${EXT}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Removing segment from $START_TIME to $END_TIME..."
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/video_remove_segment.py" "$INPUT_VIDEO" "$OUTPUT_VIDEO" "$START_TIME" "$END_TIME"

if [ $? -eq 0 ]; then
    echo "✓ Output saved to: $OUTPUT_VIDEO"
else
    echo "✗ Failed to remove segment"
    exit 1
fi
