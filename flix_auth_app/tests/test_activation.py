import pytest

from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@pytest.mark.django_db
def test_activate_user_successfully(api_client, inactive_user):
    token = default_token_generator.make_token(inactive_user)
    uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))

    url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["message"] == "Account successfully activated."

    inactive_user.refresh_from_db()
    assert inactive_user.is_active is True


@pytest.mark.django_db
def test_activate_user_invalid_token(api_client, inactive_user):
    uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))

    invalid_token = "invalidtoken123"
    url = reverse('activate', kwargs={'uidb64': uid, 'token': invalid_token})
    response = api_client.get(url)

    assert response.status_code == 400

    inactive_user.refresh_from_db()
    assert inactive_user.is_active is False


@pytest.mark.django_db
def test_activate_user_invalid_uid(api_client):
    url = reverse('activate', kwargs={'uidb64': 'INVALID_UID', 'token': 'dummy-token'})
    response = api_client.get(url)

    assert response.status_code == 400
