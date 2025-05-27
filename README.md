Deutsch
Ratewand Python Programm
Dieses private Python-Programm besteht aus zwei Anwendungen zur Steuerung und Anzeige eines interaktiven Buchstabenrätselspiels („Ratewand“). Es wurde ausschließlich für den privaten Gebrauch entwickelt.

Funktionen:

control.py: GUI zur Eingabe von Kategorien und Buchstaben in einem 4x13-Raster. Sendet die Daten per Netzwerk an die Anzeige.

display.py: Empfängt die Daten, zeigt das Puzzle mit grafischer Benutzeroberfläche an und verwaltet die Buchstabenaufdeckung. Unterstützt optionale Soundeffekte für richtige und falsche Buchstabeneingaben.

Voraussetzungen:

Betriebssystem: Windows 10 oder neuer

Python-Version: 3.7 oder höher

Installierte Python-Module:

tkinter (normalerweise vorinstalliert)

pygame (kann mit pip install pygame installiert werden)

Sounddateien:

Im Programmordner muss ein Unterordner namens sounds selbst erstellt werden.

Die Sounddateien müssen in diesem sounds-Ordner liegen und heißen genau:

buchstabe.mp3 (für korrekte Buchstaben)

kein_buchstabe.mp3 (für falsche Buchstaben)

Sound ist optional; das Programm läuft auch ohne diese Dateien.

Installation:

Installiere Python 3.7 oder höher von python.org.

Installiere die benötigten Module mit:

bash
Kopieren
Bearbeiten
pip install pygame
Lade die Dateien control.py, display.py, start.bat und diese README herunter und speichere sie im selben Ordner.

Erstelle den Ordner sounds im gleichen Ordner und füge dort die beiden MP3-Dateien ein (siehe oben).

Starte das Programm mit der start.bat, die beide Komponenten gleichzeitig startet.

Nutzung:

display.py zeigt das Puzzle an und reagiert auf Tastatureingaben.

control.py dient zur Eingabe des Puzzles und sendet es an die Anzeige.

Soundeffekte werden bei richtiger oder falscher Eingabe abgespielt (wenn vorhanden).

Hinweis:
Dieses Programm ist ausschließlich für private Zwecke bestimmt. Kommerzielle Nutzung oder Verbreitung ohne Genehmigung ist nicht erlaubt.

Kontakt:
Bei Fragen erreichst du mich unter: akhler362003@gmail.com

English
Ratewand Python Program
This private Python program consists of two applications for controlling and displaying an interactive letter puzzle game ("Ratewand"). It is intended strictly for private use.

Features:

control.py: GUI for entering categories and letters in a 4x13 grid, sending data via network to the display.

display.py: Receives data, shows the puzzle with a graphical user interface, manages letter uncovering, and supports optional sound effects for correct and incorrect letters.

Requirements:

Operating System: Windows 10 or newer

Python version: 3.7 or higher

Installed Python modules:

tkinter (usually pre-installed)

pygame (install via pip install pygame)

Sound files:

A folder named sounds must be manually created inside the program directory.

The sound files must be placed inside this sounds folder and must be named exactly:

buchstabe.mp3 (for correct letters)

kein_buchstabe.mp3 (for incorrect letters)

Sound is optional; the program runs without these files.

Installation:

Install Python 3.7 or higher from python.org.

Install the required modules:

bash
Kopieren
Bearbeiten
pip install pygame
Download the files control.py, display.py, start.bat, and this README, and save them in the same folder.

Create the sounds folder inside the same folder and add the two MP3 files (see above).

Run the program using start.bat to launch both components simultaneously.

Usage:

display.py shows the puzzle and responds to keyboard input.

control.py allows puzzle input and sends it to the display.

Sound effects play on correct or incorrect input (if available).

Note:
This program is for private use only. Commercial use or distribution without permission is prohibited.

Contact:
For questions, contact: akhler362003@gmail.com










# Ratewand Programm - README

## Deutsch

### Beschreibung
Dieses Programm besteht aus zwei Python-Anwendungen: `control.py` und `display.py`. Es handelt sich um ein privat erstelltes Programm zur Steuerung und Anzeige eines Ratewand-Spiels, bei dem ein Raster mit Buchstaben und Kategorien bearbeitet und auf einem Display angezeigt wird.

- **control.py** ist die Steuerungssoftware mit einer grafischen Oberfläche, in der Kategorien und Buchstabenraster (4x13) eingegeben und per Netzwerk an das Display gesendet werden.
- **display.py** empfängt die Daten, zeigt die Ratewand visuell an, verwaltet genutzte Buchstaben und spielt bei Buchstabeneingabe passende Sounds ab.

Das Programm ist ausschließlich für private Zwecke bestimmt und darf ohne ausdrückliche Erlaubnis nicht kommerziell genutzt werden.

### Voraussetzungen
- Betriebssystem: Windows (Getestet unter Windows 10/11)
- Python 3.7 oder höher
- Installierte Python-Module:
  - tkinter (meistens vorinstalliert)
  - pygame
- Sounddateien: `buchstabe.mp3` und `kein_buchstabe.mp3` im Ordner `sounds` im Programmverzeichnis (optional, falls nicht vorhanden, läuft das Programm trotzdem ohne Sound).

### Installation
1. Python 3.7+ von [https://python.org](https://python.org) installieren.
2. Benötigte Module installieren:
   ```bash
   pip install pygame
   ```
3. Die Programmdateien `control.py` und `display.py` in denselben Ordner legen.
4. Den Ordner `sounds` mit den Sounddateien (optional) im selben Verzeichnis anlegen.
5. Die Startdatei `start.bat` im selben Verzeichnis anlegen mit folgendem Inhalt:
   ```
   @echo off
   start python display.py
   start python control.py
   ```
6. `start.bat` ausführen, um beide Programme gleichzeitig zu starten.

### Nutzung
- Zuerst wird das Display gestartet (`display.py`), das die Ratewand anzeigt.
- Danach startet `control.py`, wo du die Kategorie und das Raster eingeben kannst.
- Änderungen in `control.py` können per Button an das Display gesendet werden.
- Im Display können Buchstaben per Tastatur aufgedeckt werden, mit Soundeffekten.

### Lizenz & Haftung
Das Programm wurde privat entwickelt und steht nur für den privaten Gebrauch zur Verfügung.  
Jegliche kommerzielle Nutzung, Vervielfältigung oder Weitergabe ohne Genehmigung ist untersagt.  
Der Autor übernimmt keine Haftung für Schäden oder Datenverlust durch Nutzung des Programms.


Für Fragen oder Support kontaktiere bitte: **akhler362003@gmail.com**

---

## English

### Description
This program consists of two Python applications: `control.py` and `display.py`. It is a privately created program for controlling and displaying a "Ratewand" puzzle game, where a grid with letters and categories is edited and shown on a display.

- **control.py** is the control software with a GUI where categories and a letter grid (4x13) can be entered and sent over the network to the display.
- **display.py** receives the data, visually shows the puzzle, manages used letters, and plays sound effects on letter input.

This program is intended for private use only and may not be used commercially without explicit permission.

### Requirements
- Operating System: Windows (tested on Windows 10/11)
- Python 3.7 or higher
- Python modules required:
  - tkinter (usually preinstalled)
  - pygame
- Sound files: `buchstabe.mp3` and `kein_buchstabe.mp3` in a `sounds` folder inside the program directory (optional, program runs without sound if missing).

### Installation
1. Install Python 3.7+ from [https://python.org](https://python.org).
2. Install required modules:
   ```bash
   pip install pygame
   ```
3. Place the program files `control.py` and `display.py` in the same folder.
4. Create a `sounds` folder with sound files (optional) in the same directory.
5. Create a `start.bat` file in the same directory with the following content:
   ```
   @echo off
   start python display.py
   start python control.py
   ```
6. Run `start.bat` to start both programs simultaneously.

### Usage
- First, start the display (`display.py`), which shows the puzzle.
- Then start `control.py` where you can enter the category and letter grid.
- Changes in `control.py` can be sent to the display with the button.
- On the display, letters can be uncovered by keyboard input with sound effects.

### License & Liability
The program was privately developed and is provided for private use only.  
Any commercial use, reproduction, or distribution without permission is prohibited.  
The author is not liable for damages or data loss from using this software.


For questions or support, please contact: **akhler362003@gmail.com**

---

### Start Script (`start.bat`)
```bat
@echo off
start python display.py
start python control.py
```

---

Vielen Dank für die Nutzung des Programms! / Thank you for using the program!





