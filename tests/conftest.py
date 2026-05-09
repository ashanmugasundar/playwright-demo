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

@pytest.fixture
def user2(db):
    return User.objects.create_user(
        username="user1",
        password="pass12345",
        email="user1@example.com",
        is_staff=False
    )

@pytest.fixture
def staff_user_2(db):
    return User.objects.create_user(
        username="staff1",
        password="pass12345",
        email="staff1@example.com",
        is_staff=True
    )

@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="user2",
        password="pass12345",
        email="user2@example.com",
        is_staff=False
    )