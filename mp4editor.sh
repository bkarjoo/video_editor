#!/bin/bash

# Get the absolute path of the script itself
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Input parameters
INPUT_VIDEO="$1"
START_TIME="$2"
END_TIME="$3"

# Determine the output video path
DIRNAME=$(dirname "$INPUT_VIDEO")
FILENAME=$(basename "$INPUT_VIDEO")
EXTENSION="${FILENAME##*.}"
BASENAME="${FILENAME%.*}"
OUTPUT_VIDEO="${DIRNAME}/${BASENAME}_edited.${EXTENSION}"

# Path to the python executable in the virtual environment
PYTHON_VENV="${SCRIPT_DIR}/venv/bin/python"

# Path to the python script
VIDEO_EDITOR_SCRIPT="${SCRIPT_DIR}/video_editor.py"

# Run the video editor script
"$PYTHON_VENV" "$VIDEO_EDITOR_SCRIPT" "$INPUT_VIDEO" "$OUTPUT_VIDEO" "$START_TIME" "$END_TIME"
