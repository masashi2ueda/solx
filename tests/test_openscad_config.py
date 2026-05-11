from pathlib import Path

import pytest

from solx.config.openscad import OpenSCADNotFoundError, get_openscad_path


def test_get_openscad_path_prefers_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENSCAD_PATH", "/custom/openscad")
    assert get_openscad_path() == "/custom/openscad"


def test_get_openscad_path_uses_path_lookup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENSCAD_PATH", raising=False)
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/openscad")
    assert get_openscad_path() == "/usr/bin/openscad"


def test_get_openscad_path_uses_macos_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENSCAD_PATH", raising=False)
    monkeypatch.setattr("shutil.which", lambda _: None)
    monkeypatch.setattr("sys.platform", "darwin")
    monkeypatch.setattr("os.name", "posix")

    candidate = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    monkeypatch.setattr(Path, "exists", lambda self: str(self) == candidate)

    assert get_openscad_path() == candidate


def test_get_openscad_path_uses_windows_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENSCAD_PATH", raising=False)
    monkeypatch.setattr("shutil.which", lambda _: None)
    monkeypatch.setattr("sys.platform", "win32")
    monkeypatch.setattr("os.name", "nt")

    candidate = r"C:\Program Files\OpenSCAD\openscad.exe"
    monkeypatch.setattr(Path, "exists", lambda self: str(self) == candidate)

    assert get_openscad_path() == candidate


def test_get_openscad_path_raises_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENSCAD_PATH", raising=False)
    monkeypatch.setattr("shutil.which", lambda _: None)
    monkeypatch.setattr("sys.platform", "linux")
    monkeypatch.setattr("os.name", "posix")
    monkeypatch.setattr(Path, "exists", lambda self: False)

    with pytest.raises(OpenSCADNotFoundError):
        get_openscad_path()
