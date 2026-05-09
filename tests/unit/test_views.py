import csv
import io
import pytest

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.test import override_settings, RequestFactory
from django.http import HttpResponse

from accounts import views


def _patch_render(monkeypatch):
    captured = {"template": None, "context": None}

    def fake_render(request, template, context):
        captured["template"] = template
        captured["context"] = context
        return HttpResponse("rendered", status=200)

    monkeypatch.setattr(views, "render", fake_render)
    return captured


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_staff_required_redirects_when_unauthenticated():
    rf = RequestFactory()
    request = rf.get("/users/export/")
    request.user = AnonymousUser()

    # users_export_csv is only @staff_required; unauth should redirect to login
    resp = views.users_export_csv(request)
    assert resp.status_code == 302
    assert "login" in resp["Location"].lower()


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_staff_required_denies_when_not_staff(user):
    rf = RequestFactory()
    request = rf.get("/users/export/")
    request.user = user

    with pytest.raises(PermissionDenied):
        views.users_export_csv(request)


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_users_export_csv_returns_csv_for_staff(staff_user, user):
    rf = RequestFactory()
    request = rf.get("/users/export/")
    request.user = staff_user

    resp = views.users_export_csv(request)
    assert resp.status_code == 200
    assert resp["Content-Type"].startswith("text/csv")
    assert "attachment; filename=" in resp["Content-Disposition"]

    content = resp.content.decode("utf-8")
    rows = list(csv.reader(io.StringIO(content)))
    assert rows[0] == ["id", "username", "email", "is_active", "is_staff"]

    # Ensure at least one known user is present in CSV rows
    usernames = [r[1] for r in rows[1:]]
    assert user.username in usernames
    assert staff_user.username in usernames


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_register_view_redirects_if_authenticated(staff_user):
    rf = RequestFactory()
    request = rf.get("/register/")
    request.user = staff_user

    resp = views.register_view(request)
    assert resp.status_code == 302  # redirect('users_list')


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_register_view_get_renders_form(monkeypatch):
    rf = RequestFactory()
    request = rf.get("/register/")
    request.user = AnonymousUser()

    captured = _patch_render(monkeypatch)

    # Fake RegisterForm class used inside view
    class FakeRegisterForm:
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr(views, "RegisterForm", FakeRegisterForm)

    resp = views.register_view(request)
    assert resp.status_code == 200
    assert captured["template"] == "accounts/register.html"
    assert "form" in captured["context"]


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
@pytest.mark.django_db
def test_register_view_post_valid_creates_user_and_redirects(monkeypatch):
    rf = RequestFactory()
    request = rf.post("/register/", data={"username": "newuser"})
    request.user = AnonymousUser()

    # avoid needing sessions/auth middleware for django.contrib.auth.login
    monkeypatch.setattr(views, "login", lambda req, u: None)

    class FakeRegisterForm:
        def __init__(self, post_data):
            self.post_data = post_data

        def is_valid(self):
            return True

        def save(self):
            return User.objects.create_user(
                username="newuser",
                password="pass12345",
                email="newuser@example.com",
            )

    monkeypatch.setattr(views, "RegisterForm", FakeRegisterForm)

    resp = views.register_view(request)
    assert resp.status_code == 302
    assert resp["Location"].endswith("/")  # users_list in accounts.urls is root


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_users_list_requires_login(monkeypatch):
    rf = RequestFactory()
    request = rf.get("/")
    request.user = AnonymousUser()

    resp = views.users_list(request)
    assert resp.status_code == 302
    assert "login" in resp["Location"].lower()


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_users_list_renders_for_authenticated(monkeypatch, user):
    rf = RequestFactory()
    request = rf.get("/")
    request.user = user

    captured = _patch_render(monkeypatch)

    resp = views.users_list(request)
    assert resp.status_code == 200
    assert captured["template"] == "accounts/users_list.html"
    assert "users" in captured["context"]
    # ordered by id, so it should contain the db users
    assert len(captured["context"]["users"]) >= 1


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_user_add_requires_login(monkeypatch):
    rf = RequestFactory()
    request = rf.get("/users/add/")
    request.user = AnonymousUser()

    resp = views.user_add(request)
    assert resp.status_code == 302
    assert "login" in resp["Location"].lower()


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_user_add_denies_non_staff(monkeypatch, user):
    rf = RequestFactory()
    request = rf.get("/users/add/")
    request.user = user

    with pytest.raises(PermissionDenied):
        views.user_add(request)


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_user_add_post_valid_staff_saves_and_redirects(monkeypatch, staff_user):
    rf = RequestFactory()
    request = rf.post("/users/add/", data={"username": "x"})
    request.user = staff_user

    # patch messages.success to avoid MessageFailure without middleware
    monkeypatch.setattr(views.messages, "success", lambda req, msg: None)

    class FakeUserManageForm:
        def __init__(self, *args, **kwargs):
            pass

        def is_valid(self):
            return True

        def save(self):
            User.objects.create_user(username="created_by_form", password="pass12345")

    monkeypatch.setattr(views, "UserManageForm", FakeUserManageForm)

    resp = views.user_add(request)
    assert resp.status_code == 302  # redirect('users_list')


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_user_edit_denies_non_staff(monkeypatch, user, another_user):
    rf = RequestFactory()
    request = rf.get(f"/users/{another_user.id}/edit/")
    request.user = user

    with pytest.raises(PermissionDenied):
        views.user_edit(request, another_user.id)


@override_settings(ROOT_URLCONF="accounts.urls")
@pytest.mark.unit
def test_user_edit_post_valid_staff_updates(monkeypatch, staff_user, another_user):
    rf = RequestFactory()
    request = rf.post(f"/users/{another_user.id}/edit/", data={"username": "updated"})
    request.user = staff_user

    monkeypatch.setattr(views.messages, "success", lambda req, msg: None)

    class FakeUserManageForm:
        def __init__(self, *args, **kwargs):
            self.instance = kwargs.get("instance")

        def is_valid(self):
            return True

        def save(self):
            self.instance.username = "updated_username"
            self.instance.save()

    monkeypatch.setattr(views, "UserManageForm", FakeUserManageForm)

    resp = views.user_edit(request, another_user.id)
    assert resp.status_code == 302
    another_user.refresh_from_db()
    assert another_user.username == "updated_username"
