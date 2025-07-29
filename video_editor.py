#!/usr/bin/env python3

import argparse
import os
import sys
from moviepy.editor import VideoFileClip


def crop_video(input_path, output_path, start_time, end_time):
    """
    Crop a video file from start_time to end_time.
    
    Args:
        input_path (str): Path to input MP4 file
        output_path (str): Path to output MP4 file
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
    
    Returns:
        bool: True if successful, False otherwise
    """
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
        
        print(f"Cropping video from {start_time}s to {end_time}s")
        cropped_video = video.subclip(start_time, end_time)
        
        print(f"Saving cropped video to: {output_path}")
        cropped_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        video.close()
        cropped_video.close()
        
        print(f"Video cropped successfully!")
        print(f"Duration: {end_time - start_time}s")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False


def parse_time(time_str):
    """
    Parse time string in various formats to seconds.
    Supports formats like: 10, 10.5, 1:30, 1:30.5, 1:30:45, 1:30:45.5
    
    Args:
        time_str (str): Time string to parse
    
    Returns:
        float: Time in seconds
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


def main():
    parser = argparse.ArgumentParser(
        description='Crop MP4 video files by specifying start and end times',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.mp4 output.mp4 10 30
  %(prog)s input.mp4 output.mp4 1:30 2:45
  %(prog)s input.mp4 output.mp4 0:30.5 1:45.5
  %(prog)s movie.mp4 clip.mp4 1:30:00 1:35:00
        """
    )
    
    parser.add_argument('input', help='Input MP4 file path')
    parser.add_argument('output', help='Output MP4 file path')
    parser.add_argument('start', help='Start time (seconds or HH:MM:SS format)')
    parser.add_argument('end', help='End time (seconds or HH:MM:SS format)')
    
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
    
    success = crop_video(args.input, args.output, start_time, end_time)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()