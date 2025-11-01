"""Główna logika asystenta do obsługi rozmów z API OpenAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from .config import AssistantConfig
from .openai_client import ChatClient, create_chat_client


@dataclass
class Assistant:
    """Wysokopoziomowy interfejs konwersacyjnego asystenta."""

    config: AssistantConfig
    _client: ChatClient = field(init=False, repr=False)
    _history: List[dict] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self._client = create_chat_client(self.config.api_key)
        if self.config.system_prompt:
            self._history.append({"role": "system", "content": self.config.system_prompt})

    @property
    def history(self) -> Iterable[dict]:
        """Zwraca historię rozmowy."""

        return tuple(self._history)

    def reset(self) -> None:
        """Czyści historię rozmowy, zachowując komunikat systemowy."""

        self._history = []
        if self.config.system_prompt:
            self._history.append({"role": "system", "content": self.config.system_prompt})

    def respond(self, user_message: str) -> str:
        """Wysyła wiadomość do asystenta i zwraca odpowiedź."""

        self._history.append({"role": "user", "content": user_message})
        response = self._client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=list(self._history),
        )
        message = response.choices[0].message.content or ""
        self._history.append({"role": "assistant", "content": message})
        return message
