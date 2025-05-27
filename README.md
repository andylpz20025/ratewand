
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
