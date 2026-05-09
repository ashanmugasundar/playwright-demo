import manage
import importlib

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

def test_manage_main_sets_env_and_calls_execute(monkeypatch):
    # Track call
    called = {}

    def fake_execute(argv):
        called["argv"] = argv

    # Patch execute
    monkeypatch.setattr(
        "django.core.management.execute_from_command_line",
        fake_execute
    )

    # Ensure env not set before
    monkeypatch.delenv("DJANGO_SETTINGS_MODULE", raising=False)
    importlib.reload(manage)  # important (fresh load)
    manage.main()

    # ✅ Check env set
    assert "DJANGO_SETTINGS_MODULE" in __import__("os").environ

    # ✅ Check function called
    assert "argv" in called
