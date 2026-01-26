import pytest
import os
import shutil

from django.urls import reverse
from django.conf import settings

from video_app.models import Video


@pytest.fixture
def hls_setup(db):
    video = Video.objects.create(title="steam", description="test")

    base_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(video.id), '480p')
    os.makedirs(base_dir, exist_ok=True)

    m3u8_path = os.path.join(base_dir, 'index.m3u8')
    with open(m3u8_path, 'w') as f:
        f.write("#EXTM3U\n#EXT-X-VERSION:3")

    ts_path = os.path.join(base_dir, 'segment0.ts')
    with open(ts_path, 'wb') as f:
        f.write(b'fakebinarydata')
    yield video

    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'hls', str(video.id)), ignore_errors=True)


@pytest.mark.django_db
def test_get_hls_playlist(api_client, user, hls_setup):
    api_client.force_authenticate(user=user)
    url = reverse('video-hls-playlist', kwargs={'video_id': hls_setup.id, 'resolution': '480p'})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/vnd.apple.mpegurl'


@pytest.mark.django_db
def test_get_hls_segment(api_client, user, hls_setup):
    api_client.force_authenticate(user=user)
    url = reverse('video-hls-segment', kwargs={
        'video_id': hls_setup.id,
        'resolution': '480p',
        'segment': 'segment0.ts'
    })
    response = api_client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'video/MP2T'


@pytest.mark.django_db
def test_streaming_fails_unauthenticated(api_client, hls_setup):
    url = reverse('video-hls-playlist', kwargs={'video_id': hls_setup.id, 'resolution': '480p'})
    response = api_client.get(url)

    assert response.status_code == 401
