# Ratewand Projekt

Dies ist die aktuelle Version der **Ratewand-App**, bestehend aus einer Steuerung (`control.py`) und einer Anzeige (`display.py`).  
Die App ermöglicht das Spielen von Rätseln, einschließlich Bonusrunden, Countdown, Sounds und Reset-Funktion.

---

## Projektstruktur

- `display.py` → Anzeige-Rätselwand, zeigt das Rätsel, LED-Rahmen, Countdown und Sound-Effekte  
- `control.py` → Steuerung der Rätsel, Eingabe von Buchstaben, Bonusrunden, Puzzleverwaltung  
- `sounds/` → Enthält alle MP3-Dateien für die Soundeffekte:
  - `buchstabe.mp3` → Ton bei richtiger Buchstabenauswahl  
  - `kein_buchstabe.mp3` → Ton bei falscher Buchstabenauswahl  
  - `new_puzzle.mp3` → Ton beim Laden eines neuen Rätsels  
  - `keinekons.mp3` → Ton wenn keine Konsonanten mehr übrig sind  
  - `geloest.mp3` → Ton bei Rätsel gelöst oder Bonusrunde gelöst  
  - `bonus.mp3` → Ton während Countdown der Bonusrunde  
  - `bonus_loes.mp3` → Ton bei Bonusrunde gelöst  
- `puzzles.json` → Gespeicherte Rätsel  
- `README.md` → Diese Anleitung

---

## Installation

1. Python 3.10+ installieren: [Python Download](https://www.python.org/downloads/)  
2. Benötigte Bibliotheken installieren:

```bash
pip install pygame


# Puzzle Board  Project

This is the current version of the **Puzzle Board  app**, consisting of a control (`control.py`) and a display (`display.py`).
The app allows you to play puzzles, including bonus rounds, a countdown, sounds, and a reset function.

---

## Project Structure

- `display.py` → Display puzzle wall, shows the puzzle, LED frame, countdown, and sound effects
- `control.py` → Control puzzles, entering letters, bonus rounds, puzzle management
- `sounds/` → Contains all MP3 files for the sound effects:
- `letter.mp3` → Sound when the correct letter is selected
- `no_letter.mp3` → Sound when the wrong letter is selected
- `new_puzzle.mp3` → Sound when a new puzzle is loaded
- `no_cons.mp3` → Sound when no more consonants remain
- `solved.mp3` → Sound when the puzzle or bonus round is solved
- `bonus.mp3` → Sound during the bonus round countdown
- `bonus_solves.mp3` → Sound when the bonus round is solved
- `puzzles.json` → Saved puzzles
- README.md → This guide

---

## Installation

1. Install Python 3.10+: [Python Download](https://www.python.org/downloads/)
2. Install required libraries:

bash
pip install pygame
