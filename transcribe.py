#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = os.path.join(SCRIPT_DIR, 'models', 'ggml-small.bin')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'cropped')


def find_whisper():
    """
    Locate the whisper.cpp command-line binary.
    Homebrew has shipped it as 'whisper-cli' (current) and 'whisper-cpp' (older).

    Returns:
        str: Path to the binary, or None if not installed
    """
    for name in ('whisper-cli', 'whisper-cpp'):
        path = shutil.which(name)
        if path:
            return path
    return None


def extract_audio(input_path, wav_path):
    """
    Extract audio as 16 kHz mono WAV, the format whisper.cpp expects.

    Args:
        input_path (str): Path to input video or audio file
        wav_path (str): Path to write the WAV file
    """
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', input_path,
        '-vn', '-ac', '1', '-ar', '16000', '-f', 'wav',
        wav_path,
    ]
    subprocess.run(cmd, check=True)


def transcribe(input_path, output_dir, model_path, language='auto', threads=None):
    """
    Transcribe a video or audio file to .txt and .srt using whisper.cpp.

    Args:
        input_path (str): Path to input video or audio file
        output_dir (str): Directory to write transcript files into
        model_path (str): Path to a ggml whisper model
        language (str): Language code, or 'auto' to detect
        threads (int): CPU threads for whisper.cpp (default: all cores)

    Returns:
        bool: True if successful, False otherwise
    """
    whisper = find_whisper()
    if not whisper:
        print("Error: whisper-cli not found. See README for build instructions.", file=sys.stderr)
        return False

    if not os.path.exists(model_path):
        print(f"Error: Model not found: {model_path}", file=sys.stderr)
        print("Download with: curl -L -o models/ggml-small.bin "
              "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin", file=sys.stderr)
        return False

    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(input_path))[0]
    output_base = os.path.join(output_dir, basename)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, 'audio.wav')

            print(f"Extracting audio from: {input_path}")
            extract_audio(input_path, wav_path)

            print(f"Transcribing with model: {os.path.basename(model_path)}")
            cmd = [
                whisper,
                '-m', model_path,
                '-f', wav_path,
                '-l', language,
                '-otxt', '-osrt',
                '-of', output_base,
                '-np',  # no progress prints; keep output to the transcript
                '-mc', '0',  # no context carry-over between windows; prevents repetition loops
            ]
            if threads:
                cmd += ['-t', str(threads)]
            subprocess.run(cmd, check=True)

        print(f"Transcript saved to: {output_base}.txt")
        print(f"Subtitles saved to:  {output_base}.srt")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.cmd[0]} exited with status {e.returncode}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe a video or audio file to text and SRT subtitles using whisper.cpp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s cropped/clip_edited.mp4
  %(prog)s recording.m4a --output-dir transcripts
  %(prog)s clip.mp4 --language en --model models/ggml-small.en.bin
  %(prog)s clip.mp4 --model models/ggml-medium.bin
        """
    )

    parser.add_argument('input', help='Input video or audio file path')
    parser.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR,
                        help='Directory for .txt and .srt output (default: cropped/)')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help='Path to ggml whisper model (default: models/ggml-small.bin)')
    parser.add_argument('--language', default='auto',
                        help="Language code (e.g. en, fa), or 'auto' to detect (default: auto)")
    parser.add_argument('--threads', type=int, default=None,
                        help='CPU threads to use (default: all cores)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not shutil.which('ffmpeg'):
        print("Error: ffmpeg not found. Install with: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)

    success = transcribe(args.input, args.output_dir, args.model, args.language, args.threads)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
