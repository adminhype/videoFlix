import os

from django.conf import settings
from django_rq import job

from .models import Video
from video_app.api.services import convert_resolution


@job
def convert_to_hls(video_id, source_path):
    "Background task to convert video to HLS format with multiple resolutions."
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
