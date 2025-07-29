# Video Editor

Simple Python tools for cropping MP4 videos with optional fade effects.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Video Cropping

```bash
python video_editor.py input.mp4 output.mp4 <start_time> <end_time>
```

### Video Cropping with Fade Effects

```bash
python video_crop_fade.py input.mp4 output.mp4 <start_time> <end_time> [--fade-in SECONDS] [--fade-out SECONDS]
```

## Time Format

- Seconds: `30` or `30.5`
- MM:SS: `1:30`
- HH:MM:SS: `1:30:45`

## Examples

```bash
# Basic crop from 10s to 30s
python video_editor.py video.mp4 clip.mp4 10 30

# Crop with 2-second fades
python video_crop_fade.py video.mp4 clip.mp4 1:30 2:45 --fade-in 2 --fade-out 2

# Crop with custom fade in only
python video_crop_fade.py video.mp4 clip.mp4 0:30 1:45 --fade-in 0.5 --fade-out 0
```

## Requirements

- Python 3.6+
- MoviePy