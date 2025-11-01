"""Pakiet asystenta dla rozwiązania OpenAI na Raspberry Pi."""

from .config import AssistantConfig, load_config

__all__ = ["Assistant", "AssistantConfig", "load_config"]


def __getattr__(name: str):  # pragma: no cover - module level laziness
    if name == "Assistant":
        from .assistant import Assistant

        return Assistant
    raise AttributeError(f"module 'assistant' has no attribute {name!r}")
