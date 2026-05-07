import pytest
from accounts.forms import RegisterForm


@pytest.mark.unit
def test_register_form_valid(db):
    form = RegisterForm(data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password1': 'ComplexPass123!',
        'password2': 'ComplexPass123!',
    })
    assert form.is_valid()


@pytest.mark.unit
def test_register_form_password_mismatch(db):
    form = RegisterForm(data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password1': 'ComplexPass123!',
        'password2': 'WrongPass',
    })
    assert not form.is_valid()
