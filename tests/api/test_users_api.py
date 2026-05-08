import pytest
from rest_framework.test import APIClient

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
