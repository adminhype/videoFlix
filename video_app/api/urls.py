from django.urls import path

from .views import VideoHLSPlaylistView, VideoHLSSegementView, VideoListView


urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:video_id>/<str:resolution>/index.m3u8',
         VideoHLSPlaylistView.as_view(), name='video-hls-playlist'),
    path('video/<int:video_id>/<str:resolution>/<str:segment>',
         VideoHLSSegementView.as_view(), name='video-hls-segment'),
]
