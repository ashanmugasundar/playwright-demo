import pytest
import manage


def test_manage_main_runs(monkeypatch):
    called = {}

    def fake_execute(argv):
        called["args"] = argv

    monkeypatch.setattr(
        "django.core.management.execute_from_command_line",
        fake_execute
    )

    manage.main()

    assert "args" in called

