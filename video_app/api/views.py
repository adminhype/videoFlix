from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import FileResponse

from video_app.models import Video
from .serializers import VideoSerializer
from .utils import get_hls_file_path


class VideoListView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Video.objects.all().order_by("-created_at")


class VideoHLSPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id, resolution):
        file_path = get_hls_file_path(video_id, resolution, "index.m3u8")
        return FileResponse(open(file_path, 'rb'), content_type="application/vnd.apple.mpegurl")


class VideoHLSSegementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id, resolution, segment):
        file_path = get_hls_file_path(video_id, resolution, segment)
        return FileResponse(open(file_path, 'rb'), content_type="video/MP2T")
