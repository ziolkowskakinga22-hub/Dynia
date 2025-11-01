"""Narzędzia konfiguracyjne dla asystenta na Raspberry Pi."""

from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

_dotenv_spec = importlib.util.find_spec("dotenv")
if _dotenv_spec is not None:  # pragma: no cover - executed when dependency present
    load_dotenv = importlib.import_module("dotenv").load_dotenv
else:  # pragma: no cover - executed when dependency absent
    def load_dotenv(*_: Any, **__: Any) -> bool:  # type: ignore[misc]
        """Zastępcze load_dotenv nic nie robi, gdy brak biblioteki python-dotenv."""

        return False

_yaml_module = importlib.util.find_spec("yaml")
if _yaml_module is not None:  # pragma: no cover - exercised when dependency present
    yaml = importlib.import_module("yaml")
else:  # pragma: no cover - executed in environments without PyYAML
    yaml = None  # type: ignore[assignment]


@dataclass
class AssistantConfig:
    """Kontener na wartości konfiguracyjne asystenta."""

    api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    system_prompt: str = ""

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any], api_key: str) -> "AssistantConfig":
        return cls(
            api_key=api_key,
            model=str(mapping.get("model", cls.model)),
            temperature=float(mapping.get("temperature", cls.temperature)),
            system_prompt=str(mapping.get("system_prompt", "")),
        )


def load_config(path: Optional[os.PathLike[str] | str] = None) -> AssistantConfig:
    """Wczytuje konfigurację z pliku YAML lub JSON oraz zmiennych środowiskowych."""

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Brak zmiennej środowiskowej OPENAI_API_KEY. Ustaw ją w powłoce lub pliku .env."
        )

    config_data: Dict[str, Any] = {}
    config_path: Optional[Path] = Path(path) if path else _default_config_path()
    if config_path and config_path.exists():
        config_data = _parse_config_file(config_path)

    return AssistantConfig.from_mapping(config_data, api_key=api_key)


def _parse_config_file(path: Path) -> Dict[str, Any]:
    """Parsuje plik konfiguracyjny przy użyciu YAML, a w razie potrzeby JSON."""

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}

    if yaml is not None:
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data  # type: ignore[return-value]
        raise ValueError("Plik konfiguracyjny musi zawierać na najwyższym poziomie mapę.")

    data = json.loads(text)
    if isinstance(data, dict):
        return data
    raise ValueError("Plik konfiguracyjny musi zawierać na najwyższym poziomie obiekt JSON.")


def _default_config_path() -> Optional[Path]:
    """Wyszukuje domyślną ścieżkę pliku konfiguracyjnego, jeśli istnieje."""

    candidates = (
        Path.cwd() / "config.yaml",
        Path.cwd() / "config.yml",
        Path(__file__).resolve().parent.parent / "config.yaml",
        Path(__file__).resolve().parent.parent / "config.json",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
