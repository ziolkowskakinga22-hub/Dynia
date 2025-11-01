# Asystent OpenAI na Raspberry Pi

Projekt udostępnia lekkiego, łatwego do rozbudowy asystenta gotowego na obsługę głosu, który może działać na Raspberry Pi i komunikować się z API OpenAI. Obecnie dostępny jest tekstowy tryb rozmowy w konsoli, a architektura pozwala w prosty sposób dodawać kolejne moduły wejścia/wyjścia (np. rozpoznawanie mowy lub integracje z GPIO).

## Funkcje

- Interfejs konwersacyjny wykorzystujący modele czatu OpenAI.
- Konfigurowalny prompt systemowy, nazwa modelu oraz temperatura poprzez plik YAML lub JSON.
- Skróty poleceń do resetowania rozmowy i zamykania programu.
- Struktura kodu przygotowana na dalszą rozbudowę o kolejne możliwości.

## Wymagania

- Python 3.11+
- Aktywny klucz OpenAI API (zmienna środowiskowa `OPENAI_API_KEY`)

Instalacja zależności:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Konfiguracja

Skopiuj plik przykładowej konfiguracji i dostosuj go do własnych potrzeb:

```bash
cp config.example.yaml config.yaml
```

> **Uwaga:** jeśli pakiet `pyyaml` nie jest zainstalowany, loader użyje parsera JSON. W takiej sytuacji upewnij się, że plik konfiguracyjny zawiera poprawny JSON.

Dostępne opcje:

- `model`: nazwa modelu czatu (domyślnie `gpt-4o-mini`).
- `temperature`: temperatura próbkowania modelu (domyślnie `0.7`).
- `system_prompt`: ogólna instrukcja prowadząca zachowanie asystenta.

## Uruchamianie asystenta

```bash
PYTHONPATH=src python -m assistant.main
```

Jeśli oficjalny pakiet `openai` nie jest zainstalowany, asystent automatycznie przełącza się na lekki tryb offline i powtarza w odpowiedzi to, co napisał użytkownik. Aby korzystać z prawdziwego API OpenAI, doinstaluj oficjalny pakiet i ustaw klucz w zmiennej środowiskowej.

W trakcie sesji dostępne są polecenia:

- `/exit` – zakończ działanie asystenta.
- `/reset` – wyczyść historię rozmowy bez zamykania programu.

## Rozszerzenie pod Raspberry Pi

Kod jest zorganizowany tak, aby łatwo dodawać nowe sterowniki wejścia/wyjścia. Aby dodać obsługę mowy na Raspberry Pi, przygotuj moduł implementujący protokół `BaseIO` (zob. `assistant/io/text.py` jako przykład) i zintegruj biblioteki takie jak `speech_recognition` (nagrywanie audio) oraz `pyttsx3` lub `aplay` (odtwarzanie odpowiedzi).

## Testy

Podstawowy zestaw testów sprawdza ładowanie konfiguracji. Uruchomisz je poleceniem:

```bash
pytest
```

## Zmienne środowiskowe

Przed uruchomieniem asystenta ustaw klucz OpenAI:

```bash
export OPENAI_API_KEY="sk-..."
```

Alternatywnie możesz umieścić klucz w pliku `.env` (szczegóły w `assistant/config.py`).

## Publikacja na GitHubie

1. **Zainicjuj repozytorium (jeśli jeszcze nie istnieje):**
   ```bash
   git init
   git branch -m main
   git add .
   git commit -m "Inicjalna wersja asystenta"
   ```
2. **Utwórz zdalne repozytorium na GitHubie**, np. wchodząc na https://github.com/new i nadając mu nazwę.
3. **Połącz lokalne repozytorium ze zdalnym:**
   ```bash
   git remote add origin git@github.com:twoja-nazwa-uzytkownika/twoje-repo.git
   ```
   lub w wersji HTTPS:
   ```bash
   git remote add origin https://github.com/twoja-nazwa-uzytkownika/twoje-repo.git
   ```
4. **Wypchnij kod na GitHuba:**
   ```bash
   git push -u origin main
   ```

Jeżeli repozytorium już istnieje, wystarczy dodać nowy zdalny adres (krok 3) i wykonać `git push`. Przy kolejnych zmianach użyj sekwencji `git add`, `git commit`, `git push`, aby aktualizować kod na GitHubie.

## Pomysły na rozwój

- Obsługa wejścia głosowego i syntezy mowy.
- Integracja z peryferiami GPIO Raspberry Pi.
- Harmonogramy i przypomnienia.
- Wsparcie dla wykonywania lokalnych poleceń systemowych.

Chętnie przyjmę sugestie i kontrybucje!
