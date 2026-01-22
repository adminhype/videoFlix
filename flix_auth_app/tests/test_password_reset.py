import pytest

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@pytest.mark.django_db
def test_password_reset_request(api_client, user):
    url = reverse("password_reset_request")

    data = {
        "email": user.email
    }
    response = api_client.post(url, data)

    assert response.status_code == 200
    assert response.data["detail"] == "An email has been sent to reset your password."


@pytest.mark.django_db
def test_password_reset_confirm_success(api_client, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
    data = {
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    }
    response = api_client.post(url, data)

    assert response.status_code == 200
    assert response.data["detail"] == "Your Password has been successfully reset."

    user.refresh_from_db()
    assert user.check_password("newpassword123") is True


@pytest.mark.django_db
def test_password_reset_mismatch(api_client, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
    data = {
        "new_password": "newpassword123",
        "confirm_password": "diffpassword123"
    }
    response = api_client.post(url, data)

    assert response.status_code == 400
