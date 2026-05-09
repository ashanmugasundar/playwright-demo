import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from accounts.permissions import IsStaffOrReadOnly

@pytest.mark.unit
def test_safe_method_requires_authenticated(user):
    factory = APIRequestFactory()
    perm = IsStaffOrReadOnly()

    req = factory.get("/anything/")
    req.user = AnonymousUser()
    assert perm.has_permission(req, None) is False

    req.user = user
    assert perm.has_permission(req, None) is True

@pytest.mark.unit
def test_unsafe_method_requires_staff(user, staff_user):
    factory = APIRequestFactory()
    perm = IsStaffOrReadOnly()

    req = factory.post("/anything/", data={})
    req.user = user
    assert perm.has_permission(req, None) is False

    req.user = staff_user
    assert perm.has_permission(req, None) is True
