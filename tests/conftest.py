import pytest
from django.contrib.auth.models import User
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="password123",
    )

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="password123",
        is_staff=True,
        # optional:
        is_superuser=True,
    )