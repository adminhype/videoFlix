import pytest

from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return "securepasswordn"


@pytest.fixture
def user(db, test_password):
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password=test_password,
        is_active=True
    )


@pytest.fixture
def inactive_user(db, test_password):
    return User.objects.create_user(
        username="inactiveuser",
        email="sleepyuser@example.com",
        password=test_password,
        is_active=False
    )
