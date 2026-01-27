import os

from django.conf import settings
from django.http import Http404


def get_hls_file_path(video_id, resolution, filename):
    """Resolves the file path for a specific HLS segment or playlist"""
    if resolution not in ["480p", "720p", "1080p"]:
        raise Http404("Resolution not supported")

    file_path = os.path.join(
        settings.MEDIA_ROOT,
        "hls",
        str(video_id),
        resolution,
        filename
    )
    if not os.path.exists(file_path):
        raise Http404("File not found")
    return file_path
