import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_login_success(api_client):
    email = "login@example.com"
    password = "securepassword123"

    User.objects.create_user(
        username="loginuser",
        email=email,
        password=password,
        is_active=True
    )

    url = reverse("login")
    data = {
        "email": email,
        "password": password
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["detail"] == "Login successful"
    assert response.data["user"]["email"] == email
    assert "access" not in response.data
    assert "refresh" not in response.data
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


@pytest.mark.django_db
def test_login_fail_wrong_password(api_client):
    email = "wrong@example.com"

    User.objects.create_user(
        username="wronguser",
        email=email,
        password="correctpassword",
        is_active=True
    )
    url = reverse("login")
    data = {
        "email": email,
        "password": "wrongpassword"
    }
    response = api_client.post(url, data)

    assert response.status_code == 401
