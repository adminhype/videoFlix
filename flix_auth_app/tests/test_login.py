import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_login_success(api_client, user, test_password):
    url = reverse("login")

    data = {
        "email": user.email,
        "password": test_password
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["detail"] == "Login successful"
    assert response.data["user"]["email"] == user.email
    assert "access" not in response.data
    assert "refresh" not in response.data
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.django_db
def test_login_fail_wrong_password(api_client, user):
    url = reverse("login")

    data = {
        "email": user.email,
        "password": "wrongpassword"
    }
    response = api_client.post(url, data)

    assert response.status_code == 401
