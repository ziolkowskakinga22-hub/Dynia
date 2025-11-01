"""Punkt wejścia do uruchamiania asystenta OpenAI na Raspberry Pi."""

from __future__ import annotations

from assistant import Assistant, load_config
from assistant.io import TextIO

EXIT_COMMANDS = {"/exit", "quit", "q"}
RESET_COMMANDS = {"/reset"}


def _handle_command(command: str, assistant: Assistant, io: TextIO) -> bool:
    normalized = command.strip().lower()
    if normalized in EXIT_COMMANDS:
        io.notify("Zamykanie asystenta. Do zobaczenia!")
        return False
    if normalized in RESET_COMMANDS:
        assistant.reset()
        io.notify("Historia rozmowy została zresetowana.")
        return True
    io.notify("Nieznane polecenie. Dostępne: /reset, /exit")
    return True


def main() -> None:
    config = load_config()
    assistant = Assistant(config)
    io = TextIO()
    io.notify("Witaj! Możesz rozmawiać z asystentem. Użyj /exit aby zakończyć, /reset aby wyczyścić historię.")

    running = True
    while running:
        user_message = io.read().strip()
        if not user_message:
            continue
        if user_message.startswith("/"):
            running = _handle_command(user_message, assistant, io)
            continue
        reply = assistant.respond(user_message)
        io.write(reply)


if __name__ == "__main__":
    main()
