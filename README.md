# Video Editor

Command-line tools for trimming MP4 videos (with optional fades), removing a middle segment, and transcribing speech to text.

## Status

Working. Trim, fade, segment removal and transcription all tested on Zoom recordings.

## Installation

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt   # MoviePy 1.0.3 (2.x is not compatible)
brew install ffmpeg cmake
# whisper.cpp — build from source (Homebrew has no Intel Mac bottles)
git clone --depth 1 --branch v1.9.5 https://github.com/ggml-org/whisper.cpp.git ~/dev/whisper.cpp-src
cmake -S ~/dev/whisper.cpp-src -B ~/dev/whisper.cpp-src/build -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=OFF
cmake --build ~/dev/whisper.cpp-src/build -j
cmake --install ~/dev/whisper.cpp-src/build --prefix /usr/local   # puts whisper-cli on PATH
mkdir -p models
curl -L -o models/ggml-small.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
```

## Usage

### Trim (keep a section)

```bash
venv/bin/python video_editor.py input.mp4 output.mp4 <start> <end>
./mp4editor.sh input.mp4 <start> <end>        # writes input_edited.mp4 next to input
```

### Trim with fades

```bash
venv/bin/python video_crop_fade.py input.mp4 output.mp4 <start> <end> [--fade-in SECONDS] [--fade-out SECONDS]
```

Fades apply to video only; audio does not fade.

### Remove a segment (cut out the middle)

```bash
venv/bin/python video_remove_segment.py input.mp4 output.mp4 <start> <end>
./remove_segment.sh input.mp4 <start> <end>   # writes input_edited.mp4 next to input
```

### Transcribe

```bash
./transcribe.py input.mp4 [--output-dir DIR] [--model PATH] [--language auto|en|fa|...] [--threads N]
```

Writes `<name>.txt` and `<name>.srt` to `cropped/` by default. Accepts any video or audio file ffmpeg can read. Language is auto-detected by default; the model is multilingual.

## Time Format

- Seconds: `30` or `30.5`
- MM:SS: `1:30` or `3:24.5`
- HH:MM:SS: `1:30:45`

## Layout

- `cropped/` — finished cuts and transcripts (not tracked in git)
- `models/` — Whisper models (not tracked in git)

## Requirements

- Python 3.6+, MoviePy 1.0.3
- ffmpeg
- whisper.cpp 1.9.5, built from source (for transcription)
