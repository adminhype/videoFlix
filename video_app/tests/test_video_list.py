import pytest

from django.urls import reverse

from video_app.models import Video


@pytest.mark.django_db
def test_get_video_list_auth(api_client, user):
    Video.objects.create(
        title="video1",
        description="desc1",
        category="Drama"
    )
    Video.objects.create(
        title="video2",
        description="desc2",
        category="Comedy"
    )

    api_client.force_authenticate(user=user)

    url = reverse("video-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["title"] == "video2"


@pytest.mark.django_db
def test_get_video_list_unauth(api_client):
    url = reverse("video-list")
    response = api_client.get(url)

    assert response.status_code == 401
