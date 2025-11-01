# Raspberry Pi OpenAI Assistant

This project provides a lightweight, extensible voice-ready assistant that can run on a Raspberry Pi and communicate with the OpenAI API. The assistant currently supports a text-based console conversation loop and is structured to allow new input/output modalities (such as speech recognition or GPIO interactions) to be added later.

## Features

- Conversational interface using OpenAI chat models.
- Configurable system prompt, model name, and temperature via YAML or JSON configuration.
- Command shortcuts for resetting the conversation or exiting the assistant.
- Structured codebase designed for easy extension with additional capabilities.

## Requirements

- Python 3.11+
- An active OpenAI API key (`OPENAI_API_KEY` environment variable)

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy the example configuration file and adjust it to your needs:

```bash
cp config.example.yaml config.yaml
```

> **Note:** If `pyyaml` is not installed the loader falls back to JSON parsing. In that case ensure your configuration file contains valid JSON content.

Available configuration options:

- `model`: Chat model to use (default: `gpt-4o-mini`).
- `temperature`: Sampling temperature for the model (default: `0.7`).
- `system_prompt`: A high-level instruction that guides the assistant's behavior.

## Running the Assistant

```bash
PYTHONPATH=src python -m assistant.main
```

If the official `openai` package is not installed the assistant automatically
falls back to a lightweight offline stub that simply echoes back what you said.
Install the real SDK to connect to the OpenAI API when you have internet
access.

Within the session you can use the following commands:

- `/exit` – quit the assistant.
- `/reset` – clear the conversation history while keeping the assistant running.

## Extending for Raspberry Pi

The code is organized to make it easy to add new input/output providers. To add voice interaction on a Raspberry Pi, create a new module that implements the `BaseIO` protocol (see `assistant/io/text.py` for a reference implementation) and integrate libraries such as `speech_recognition` for capturing audio and `pyttsx3` or aplay for playback.

## Testing

The project includes a basic test suite that validates configuration loading. Run the tests with:

```bash
pytest
```

## Environment Variables

Set your OpenAI API key before running the assistant:

```bash
export OPENAI_API_KEY="sk-..."
```

Alternatively, you can place the key in a `.env` file (see `assistant/config.py` for details).

## Roadmap Ideas

- Voice input and text-to-speech output.
- Integration with Raspberry Pi GPIO peripherals.
- Scheduling and reminders.
- Support for local command execution.

Contributions and suggestions are welcome!
