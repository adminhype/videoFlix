import pytest

from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse


@pytest.mark.django_db
def test_logout_success(api_client, user):
    refresh = RefreshToken.for_user(user)

    api_client.cookies["refresh_token"] = str(refresh)
    api_client.cookies["access_token"] = str(refresh.access_token)

    url = reverse("logout")
    response = api_client.post(url)

    assert response.status_code == 200
    assert "Logout successful!" in response.data["detail"]
    assert response.cookies["refresh_token"].value == ""


@pytest.mark.django_db
def test_logout_fails_without_token(api_client):
    url = reverse("logout")
    response = api_client.post(url)

    assert response.status_code == 400
    assert response.data["detail"] == "Refresh token required."
