import json
import os
import subprocess


def convert_resolution(source, base_dir, resu_name, scale, bitrate):
    """ Executes FFmpeg to convert a video file to a specific resolution and bitrate"""
    output_dir = os.path.join(base_dir, resu_name)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "index.m3u8")

    cmd = [
        'ffmpeg',
        '-i', source,
        '-vf', f'scale={scale}',
        '-c:v', 'libx264',
        '-b:v', bitrate,
        '-preset', 'veryfast',
        '-g', '60',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-pix_fmt', 'yuv420p',
        '-f', 'hls',
        output_file
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def capture_frame(source, output_path):
    """Extracts a single frame from a video at the 1 second mark."""
    cmd = [
        'ffmpeg',
        '-i', source,
        '-ss', '00:00:01',
        '-vframes', '1',
        '-q:v', '2',
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_video_height(source_path):
    """reads the height of a video file using FFprobe."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=height',
        '-of', 'json',
        source_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return int(data['streams'][0]['height'])
    except (KeyError, IndexError, ValueError, subprocess.CalledProcessError):
        return 0
