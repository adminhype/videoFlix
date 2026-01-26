import os
import subprocess

from django.conf import settings
from django_rq import job

from .models import Video


@job
def convert_to_hls(video_id, source_path):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return

    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(video_id))
    os.makedirs(base_dir, exist_ok=True)

    convert_resolution(source_path, base_dir, "480p", "-2:480", "800k")

    convert_resolution(source_path, base_dir, "720p", "-2:720", "1500k")
    video.has_720p = True

    convert_resolution(source_path, base_dir, "1080p", "-2:1080", "3000k")
    video.has_1080p = True

    video.save()


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
        '-preset', 'fast',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-f', 'hls', output_file
    ]

    subprocess.run(cmd, check=True)
