import pytest
from pathlib import Path

pytestmark = pytest.mark.e2e


def ui_login(page, base_url, username, password):
    page.goto(base_url + "/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button:has-text("Login")')
    page.wait_for_url("**/users/**")


def test_non_staff_forbidden_add_edit_export(live_server, page, user):
    base = live_server.url

    # login as normal user
    ui_login(page, base, "alice", "password123")

    # Add User link should not exist
    assert page.locator('[data-testid="nav-add-user-btn"]').count() == 0
    assert page.locator('[data-testid="nav-export-users-btn"]').count() == 0

    # Direct URL access should be forbidden (403)
    resp = page.goto(base + "/users/add/")
    assert resp.status == 403

    resp = page.goto(base + "/users/export/")
    assert resp.status == 403


def test_staff_can_add_edit_and_export_csv(live_server, page, staff_user, db):
    base = live_server.url

    # login as staff user
    ui_login(page, base, "admin", "password123")

    # Add a user
    # Add User
    page.click('[data-testid="nav-add-user-btn"]')
    page.fill('input[name="username"]', "csvuser")
    page.fill('input[name="email"]', "csvuser@example.com")
    page.check('input[name="is_active"]')
    page.uncheck('input[name="is_staff"]')
    page.click('button:has-text("Save")')
    page.wait_for_selector("text=User created.")

    # Edit first user (use first edit icon)
    # If you used edit-user-btn-<id>, pick by CSS prefix:
    first_edit = page.locator('[data-testid^="edit-user-btn-"]').first
    first_edit.click()
    page.fill('input[name="email"]', "updated@example.com")
    page.click('button:has-text("Save")')
    page.wait_for_selector("text=User updated.")

    # Export CSV and verify download
    with page.expect_download() as dl_info:
        page.click('[data-testid="nav-export-users-btn"]')

    download = dl_info.value
    out = Path("users.csv")
    download.save_as(out)
    csv_text = out.read_text(encoding="utf-8")

    assert "id,username,email,is_active,is_staff" in csv_text
    assert "csvuser" in csv_text