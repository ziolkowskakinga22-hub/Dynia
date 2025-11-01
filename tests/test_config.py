from __future__ import annotations

from pathlib import Path

import pytest

from assistant.config import AssistantConfig, load_config


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")


def test_load_config_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert isinstance(config, AssistantConfig)
    assert config.model == "gpt-4o-mini"
    assert config.temperature == 0.7
    assert config.system_prompt == ""
    assert config.api_key == "test-key"


def test_load_config_from_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
{
  "model": "gpt-4.1-mini",
  "temperature": 0.3,
  "system_prompt": "Test prompt."
}
"""
    )
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert config.model == "gpt-4.1-mini"
    assert config.temperature == pytest.approx(0.3)
    assert config.system_prompt.strip() == "Test prompt."


def test_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        load_config()
