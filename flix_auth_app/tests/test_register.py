import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_register_user_successfully(api_client):

    # url = reverse('register')
    url = "/api/register/"
    data = {
        "email": "apiuser@example.com",
        "password": "apiuserpassword",
        "confirmed_password": "apiuserpassword"
    }
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data == {"detail": "User Created successfully!"}
    assert User.objects.filter(username="apiuser").exists()


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    # url = reverse('register')
    url = "/api/register/"
    data = {
        "email": "failuser@example.com",
        "password": "password123",
        "confirmed_password": "password321"
    }
    response = api_client.post(url, data)

    assert response.status_code == 400
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_register_duplicate_email(api_client):
    User.objects.create_user(username="dup", email="duplicate@example.com", password="password123")
    url = "/api/register/"
    # url = reverse('register')
    data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "confirmed_password": "password123"
    }
    response = api_client.post(url, data)

    assert response.status_code == 400
    assert User.objects.count() == 1
