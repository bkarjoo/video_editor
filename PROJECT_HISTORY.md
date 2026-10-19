# Project History

## 2026-10-19

- Added `transcribe.py`: extracts audio with ffmpeg, transcribes with whisper.cpp, writes `.txt` and `.srt` to `cropped/`.
- Built whisper.cpp 1.9.5 from source in `~/dev/whisper.cpp-src` and installed to `/usr/local` (Homebrew install failed: no Intel bottles, source build broke on `sphinx-doc`). Downloaded `ggml-small.bin` (multilingual) to `models/` (gitignored); `small.en` returned "(speaks in foreign language)" on the test recording.
- Added `cropped/` as the output folder for finished cuts.
- Committed `mp4editor.sh` wrapper (was untracked).
- Pulled `video_remove_segment.py` and `remove_segment.sh` from remote (committed elsewhere).
- Rewrote README; added PROJECT_HISTORY.md and TODO.md.
- Tested trim and fade on a 32-minute Zoom recording: 3:24.5–21:49 cut took ~1.5 min.
- Tested transcriber on a 10 s clip: Arabic auto-detected and transcribed correctly; ~0.9× real time on Intel CPU (16 threads).

## 2025-07-29

- Initial commit: `video_editor.py` (trim) and `video_crop_fade.py` (trim with fades).
- Added README.
