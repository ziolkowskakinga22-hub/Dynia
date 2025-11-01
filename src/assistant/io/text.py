"""Implementacja wejścia/wyjścia oparta na konsoli."""

from __future__ import annotations

import sys
from typing import Optional

from .base import BaseIO


class TextIO(BaseIO):
    """Prosty dostawca I/O korzystający z stdin/stdout."""

    def __init__(self, prompt: str = "you> ", stream: Optional[object] = None) -> None:
        self.prompt = prompt
        self.stream = stream or sys.stdout

    def read(self) -> str:
        try:
            return input(self.prompt)
        except EOFError:
            return "/exit"

    def write(self, message: str) -> None:
        self.stream.write(f"assistant> {message}\n")
        self.stream.flush()

    def notify(self, message: str) -> None:
        self.stream.write(f"[info] {message}\n")
        self.stream.flush()
