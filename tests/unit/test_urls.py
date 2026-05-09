import pytest
from django.test import override_settings
from django.urls import reverse, resolve

from accounts import views


@pytest.mark.unit
@override_settings(ROOT_URLCONF="accounts.urls")
def test_named_urls_resolve():
    # '' path points to users_list
    assert resolve("/").func == views.users_list

    assert resolve("/register/").func == views.register_view
    # Django auth views: we just confirm reversing works
    reverse("login")
    reverse("logout")

    # Duplicate users_list path exists at /users/ too
    assert resolve("/users/").func == views.users_list

    assert resolve("/users/add/").func == views.user_add
    assert resolve("/users/1/edit/").func == views.user_edit
    assert resolve("/users/export/").func == views.users_export_csv


@pytest.mark.unit
@override_settings(ROOT_URLCONF="accounts.urls")
def test_drf_router_names_exist():
    # router.register(r'users', views.UserViewSet, basename='user')
    reverse("user-list")
    reverse("user-detail", kwargs={"pk": 1})
