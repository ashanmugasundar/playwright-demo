import pytest
from accounts.serializers import UserSerializer


@pytest.mark.unit
def test_user_serializer_fields(user):
    data = UserSerializer(user).data
    assert set(data.keys()) == {"id", "username", "email", "is_active", "is_staff"}
    assert data["id"] == user.id
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["is_active"] == user.is_active
    assert data["is_staff"] == user.is_staff
