import pytest
from rest_framework.test import APIClient
from django.test import override_settings
from django.urls import reverse

@pytest.mark.api
@pytest.mark.django_db
def test_users_list_requires_auth():
    client = APIClient()
    resp = client.get('/api/users/')
    assert resp.status_code in (401, 403)

@pytest.mark.api
@pytest.mark.django_db
def test_users_list_with_session_auth(client, user):
    assert client.login(username='alice', password='password123')
    resp = client.get('/api/users/')
    assert resp.status_code == 200

@pytest.mark.api
@pytest.mark.django_db
def test_create_user_via_api(client, staff_user):
    assert client.login(username='admin', password='password123')
    resp = client.post('/api/users/', {
        'username': 'charlie',
        'email': 'charlie@example.com'
    })
    assert resp.status_code == 201


@pytest.mark.api
@pytest.mark.django_db
@override_settings(ROOT_URLCONF="accounts.urls")
def test_api_users_list_requires_auth():
    client = APIClient()
    url = reverse("user-list")
    resp = client.get(url)
    assert resp.status_code in (401, 403)


@pytest.mark.api
@pytest.mark.django_db
@override_settings(ROOT_URLCONF="accounts.urls")
def test_api_users_list_allows_authenticated_get(user):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user-list")
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.api
@pytest.mark.django_db
@override_settings(ROOT_URLCONF="accounts.urls")
def test_api_users_post_denied_for_non_staff(user):
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("user-list")
    resp = client.post(url, data={"username": "a", "email": "a@a.com", "is_active": True, "is_staff": False}, format="json")
    assert resp.status_code in (401, 403)


@pytest.mark.api
@pytest.mark.django_db
@override_settings(ROOT_URLCONF="accounts.urls")
def test_api_users_post_allowed_for_staff(staff_user):
    client = APIClient()
    client.force_authenticate(user=staff_user)
    url = reverse("user-list")
    resp = client.post(url, data={"username": "new_api_user", "email": "new@api.com", "is_active": True, "is_staff": False}, format="json")
    assert resp.status_code in (200, 201)
