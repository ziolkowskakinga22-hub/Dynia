"""Narzędzia do tworzenia klienta rozmów kompatybilnego z OpenAI.

Prawdziwy pakiet `openai` nie może zostać zainstalowany w tym środowisku,
ponieważ ruch sieciowy na zewnątrz jest blokowany. Aby zachować możliwość
uruchamiania asystenta, dostarczamy niewielką atrapę udającą te fragmenty SDK,
z których korzysta aplikacja. Gdy oficjalny pakiet jest dostępny, zostanie
użyty zamiast atrapy.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import importlib.util
from typing import List, MutableMapping, Protocol


class ChatClient(Protocol):
    """Podzbiór klienta OpenAI używanego przez aplikację."""

    class _ChatNamespace(Protocol):
        class _CompletionsNamespace(Protocol):
            def create(
                self,
                *,
                model: str,
                temperature: float,
                messages: List[MutableMapping[str, str]],
            ) -> "ChatCompletion":
                ...

        completions: _CompletionsNamespace

    chat: _ChatNamespace


@dataclass
class ChatMessage:
    content: str


@dataclass
class ChatChoice:
    message: ChatMessage


@dataclass
class ChatCompletion:
    choices: List[ChatChoice]


class _StubCompletions:
    """Tryb offline, który odsyła ostatnią wiadomość użytkownika."""

    def create(
        self,
        *,
        model: str,
        temperature: float,
        messages: List[MutableMapping[str, str]],
    ) -> ChatCompletion:
        # Wyszukujemy ostatnią wiadomość użytkownika, aby przygotować prostą odpowiedź.
        # Jeśli nie znajdziemy żadnej wiadomości, odsyłamy neutralne potwierdzenie.
        last_user = next(
            (msg["content"] for msg in reversed(messages) if msg.get("role") == "user"),
            "",
        )
        reply = (
            "(tryb offline) Otrzymałem Twoją wiadomość, ale nie mogę połączyć się z API OpenAI. "
            f"Powiedziałeś: {last_user}"
        )
        return ChatCompletion(choices=[ChatChoice(message=ChatMessage(content=reply))])


class _StubChat:
    def __init__(self) -> None:
        self.completions = _StubCompletions()


class _StubOpenAI:
    def __init__(self, api_key: str) -> None:  # noqa: D401 - zachowujemy sygnaturę konstruktora
        self.api_key = api_key
        self.chat = _StubChat()


def _load_real_client(api_key: str) -> ChatClient | None:
    """Ładuje prawdziwego klienta OpenAI, jeśli pakiet jest dostępny."""

    spec = importlib.util.find_spec("openai")
    if spec is None:
        return None

    module = importlib.import_module("openai")
    openai_cls = getattr(module, "OpenAI", None)
    if openai_cls is None:
        return None

    return openai_cls(api_key=api_key)


def create_chat_client(api_key: str) -> ChatClient:
    """Zwraca klienta rozmów kompatybilnego z OpenAI lub atrapę w razie potrzeby."""

    real_client = _load_real_client(api_key)
    if real_client is not None:
        return real_client

    return _StubOpenAI(api_key=api_key)

