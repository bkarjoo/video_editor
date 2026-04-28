#!/usr/bin/env python3

import argparse
import os
import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips


def parse_time(time_str):
    """
    Parse time string in various formats to seconds.
    Supports formats like: 10, 10.5, 1:30, 1:30.5, 1:30:45, 1:30:45.5
    """
    if ':' not in time_str:
        return float(time_str)

    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        raise ValueError(f"Invalid time format: {time_str}")


def remove_segment(input_path, output_path, start_time, end_time):
    """
    Remove the segment between start_time and end_time from the video,
    concatenating the surviving head and tail into a new file.
    """
    video = None
    head = None
    tail = None
    final = None
    try:
        print(f"Loading video: {input_path}")
        video = VideoFileClip(input_path)
        duration = video.duration

        if start_time < 0:
            raise ValueError(f"Start time cannot be negative: {start_time}")
        if end_time > duration:
            raise ValueError(f"End time ({end_time}s) exceeds video duration ({duration}s)")
        if start_time >= end_time:
            raise ValueError(f"Start time ({start_time}s) must be less than end time ({end_time}s)")

        print(f"Removing segment from {start_time}s to {end_time}s (duration {duration}s)")

        pieces = []
        if start_time > 0:
            head = video.subclip(0, start_time)
            pieces.append(head)
        if end_time < duration:
            tail = video.subclip(end_time, duration)
            pieces.append(tail)

        if not pieces:
            raise ValueError("Removal range covers the entire video; nothing left to write")

        if len(pieces) == 1:
            final = pieces[0]
        else:
            final = concatenate_videoclips(pieces)

        print(f"Saving edited video to: {output_path}")
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')

        print("Video edited successfully!")
        print(f"New duration: {final.duration}s")
        return True

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False

    finally:
        for clip in (final, head, tail, video):
            if clip is not None:
                try:
                    clip.close()
                except Exception:
                    pass


def main():
    parser = argparse.ArgumentParser(
        description='Remove a segment from an MP4 video by specifying start and end times to delete',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp4 output.mp4 10 30
  %(prog)s input.mp4 output.mp4 1:30 2:45
  %(prog)s movie.mp4 edited.mp4 1:30:00 1:35:00
        """
    )

    parser.add_argument('input', help='Input MP4 file path')
    parser.add_argument('output', help='Output MP4 file path')
    parser.add_argument('start', help='Start time of segment to remove (seconds or HH:MM:SS)')
    parser.add_argument('end', help='End time of segment to remove (seconds or HH:MM:SS)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not args.input.lower().endswith('.mp4'):
        print("Warning: Input file does not have .mp4 extension")

    try:
        start_time = parse_time(args.start)
        end_time = parse_time(args.end)
    except ValueError as e:
        print(f"Error parsing time: {e}", file=sys.stderr)
        sys.exit(1)

    success = remove_segment(args.input, args.output, start_time, end_time)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
