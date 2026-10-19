# TODO

- Fade audio along with video in `video_crop_fade.py` (`audio_fadein` / `audio_fadeout`).
- Make `mp4editor.sh` and `remove_segment.sh` write to `cropped/` instead of next to the input.
- Add `--fade-in` / `--fade-out` passthrough to `mp4editor.sh`.
- Warn before overwriting an existing output file.
- Use `ffmpeg -c copy` for trims without fades (fast, lossless).
- Merge duplicated `parse_time()` into a shared module; reject values like `1:75`.
- Close clips in `finally` so files are released on error.
- Try `ggml-medium.bin` for mixed Arabic/English recordings; `small` sometimes hears English as Arabic (roughly 3× slower).
- Transcription runs ~real time on this Intel CPU; consider `-DGGML_METAL=ON` or faster-whisper if too slow.
