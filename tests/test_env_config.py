import importlib

import pytest


def test_env_config_output_dir_is_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OUTPUT_STL_DIR_PATH", raising=False)

    env_module = importlib.import_module("solx.config.env")
    importlib.reload(env_module)

    assert env_module.EnvConfig.OUTPUT_STL_DIR_PATH is None
    assert env_module.EnvConfig.get_output_stl_dir_path() == "output_stl"


def test_env_config_output_dir_uses_env_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OUTPUT_STL_DIR_PATH", "/tmp/stl")

    env_module = importlib.import_module("solx.config.env")
    importlib.reload(env_module)

    assert env_module.EnvConfig.OUTPUT_STL_DIR_PATH == "/tmp/stl"
    assert env_module.EnvConfig.get_output_stl_dir_path() == "/tmp/stl"
