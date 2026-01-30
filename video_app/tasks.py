import os

from django.conf import settings
from django.core.files import File
from django_rq import job

from .models import Video
from video_app.api.services import convert_resolution, capture_frame


@job
def convert_to_hls(video_id, source_path):
    "Background task to convert video to HLS format with multiple resolutions."
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return

    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(video_id))
    os.makedirs(base_dir, exist_ok=True)

    generate_thumbail(video, source_path, base_dir)

    convert_resolution(source_path, base_dir, "480p", "-2:480", "800k")
    convert_resolution(source_path, base_dir, "720p", "-2:720", "1500k")
    video.has_720p = True

    convert_resolution(source_path, base_dir, "1080p", "-2:1080", "3000k")
    video.has_1080p = True

    video.save()


def generate_thumbail(video, source_path, base_dir):
    """Generates and saves a thumbnail if none exists."""
    if not video.thumbnail:
        thumb_path = os.path.join(base_dir, f"{video.id}_thumbnail.jpg")
        capture_frame(source_path, thumb_path)

        if os.path.exists(thumb_path):
            with open(thumb_path, "rb") as thumb_file:
                video.thumbnail.save(f"{video.id}.jpg", File(thumb_file), save=False)
            os.remove(thumb_path)