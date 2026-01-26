import os
import subprocess


def convert_resolution(source, base_dir, resu_name, scale, bitrate):
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
        '-f', 'hls', output_file
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
