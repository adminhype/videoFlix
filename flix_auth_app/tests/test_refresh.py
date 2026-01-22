import pytest

from rest_framework_simplejwt.tokens import RefreshToken

from django.urls import reverse


@pytest.mark.django_db
def test_token_refresh_success(api_client, user):
    refresh = RefreshToken.for_user(user)

    api_client.cookies["refresh_token"] = str(refresh)

    url = reverse("token_refresh")
    response = api_client.post(url)

    assert response.status_code == 200
    assert response.data["detail"] == "Token refreshed"
    assert "access_token" in response.cookies
    assert "access" in response.data


@pytest.mark.django_db
def test_token_refresh_missing_cookie(api_client):
    url = reverse("token_refresh")
    response = api_client.post(url)

    assert response.status_code == 400
    assert response.data["detail"] == "Refresh token required"


@pytest.mark.django_db
def test_token_refresh_invalid_cookie(api_client):
    api_client.cookies["refresh_token"] = "invalid_token"
    url = reverse("token_refresh")
    response = api_client.post(url)

    assert response.status_code == 401
    assert response.data["detail"] == "Invalid refresh token"
