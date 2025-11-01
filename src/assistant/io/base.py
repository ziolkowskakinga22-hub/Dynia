"""Abstrakcyjne definicje dla mechanizmów wejścia/wyjścia asystenta."""

from __future__ import annotations

from typing import Protocol


class BaseIO(Protocol):
    """Protokół dla dostawców I/O używanych przez asystenta."""

    def read(self) -> str:
        """Pobiera dane wejściowe od użytkownika."""

    def write(self, message: str) -> None:
        """Wyświetla wiadomość dla użytkownika."""

    def notify(self, message: str) -> None:
        """Pokazuje informację niezwiązaną bezpośrednio z odpowiedzią asystenta."""
