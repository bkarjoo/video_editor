# TODO

- Fade audio along with video in `video_crop_fade.py` (`audio_fadein` / `audio_fadeout`).
- Make `mp4editor.sh` and `remove_segment.sh` write to `cropped/` instead of next to the input.
- Add `--fade-in` / `--fade-out` passthrough to `mp4editor.sh`.
- Warn before overwriting an existing output file.
- Use `ffmpeg -c copy` for trims without fades (fast, lossless).
- Merge duplicated `parse_time()` into a shared module; reject values like `1:75`.
- Close clips in `finally` so files are released on error.
- Try `ggml-medium.en.bin` if `small.en` accuracy is insufficient (roughly 3× slower, 1.5 GB).
- Suppress hallucinated English during non-English stretches (e.g. whisper-cli `--entropy-thold` / `--no-speech-thold`, or drop consecutive duplicate segments in post).
- Delete unused `models/ggml-small.bin` if no non-English transcription is needed.
- Transcription runs ~real time on this Intel CPU; consider `-DGGML_METAL=ON` or faster-whisper if too slow.
