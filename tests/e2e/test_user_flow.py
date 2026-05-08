import pytest

pytestmark = pytest.mark.e2e


def test_register_login_logout(live_server, page):
    base = live_server.url

    # Register
    page.goto(base + '/register/')
    page.fill('input[name="username"]', 'e2euser')
    page.fill('input[name="email"]', 'e2euser@example.com')
    page.fill('input[name="password1"]', 'ComplexPass123!')
    page.fill('input[name="password2"]', 'ComplexPass123!')
    page.click('button:has-text("Create Account")')

    # Should land on Users page
    page.wait_for_selector('[data-testid="nav-users-btn"]')

    # Logout
    page.click('text=Logout')
    page.wait_for_url("**/login/")


def test_staff_user_login_manage_logout(live_server, page, staff_user):
    base = live_server.url

    # Register
    page.goto(base + '/login/')
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'password123')
    page.click('button:has-text("Login")')

    assert page.url.endswith("/users/")

    # Should land on Users page
    page.wait_for_selector('[data-testid="nav-users-btn"]')

    # Add a user
    page.click('[data-testid="nav-add-user-btn"]')
    page.fill('input[name="username"]', 'newuser')
    page.fill('input[name="email"]', 'newuser@example.com')
    page.uncheck('input[name="is_staff"]')
    page.check('input[name="is_active"]')
    page.click('button:has-text("Save")')
    page.wait_for_selector('text=User created.')

    # Edit the first user (Edit link)
    page.locator('[data-testid^="edit-user-btn-"]').first.click()
    page.fill('input[name="email"]', 'updated@example.com')
    page.click('button:has-text("Save")')
    page.wait_for_selector('text=User updated.')

    # Logout
    page.click('text=Logout')
    page.wait_for_url("**/login/")
