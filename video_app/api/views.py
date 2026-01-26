from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from video_app.models import Video

from .serializers import VideoSerializer


class VideoListView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Video.objects.all().order_by("-created_at")
