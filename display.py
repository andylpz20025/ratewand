import tkinter as tk
import threading
import socket
import json
import time
import pygame
import os

ROWS, COLS = 4, 13
HOST = "127.0.0.1"
PORT = 65432

SOUND_PATH = r"C:\Users\andre\Desktop\Neuer Ordner (3)\000\ratewand\sounds"

class DisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ratewand Display")
        self.configure(bg="#000000")

        pygame.mixer.init()

        # Lade Sounds, falls vorhanden
        try:
            self.sound_buchstabe = pygame.mixer.Sound(os.path.join(SOUND_PATH, "buchstabe.mp3"))
        except Exception as e:
            print("Fehler beim Laden von buchstabe.mp3:", e)
            self.sound_buchstabe = None
        try:
            self.sound_kein_buchstabe = pygame.mixer.Sound(os.path.join(SOUND_PATH, "kein_buchstabe.mp3"))
        except Exception as e:
            print("Fehler beim Laden von kein_buchstabe.mp3:", e)
            self.sound_kein_buchstabe = None

        # Leeres Puzzle
        self.puzzle = [["" for _ in range(COLS)] for _ in range(ROWS)]
        self.revealed = [[False]*COLS for _ in range(ROWS)]
        self.used_letters = set()
        self.category = ""

        self.create_widgets()
        self.start_server_thread()

        self.bind("<Key>", self.on_key_press)

        self.lock = threading.Lock()
        self.is_uncovering = False

    def create_widgets(self):
        self.category_label = tk.Label(self, text="Kategorie: ", font=("Arial Black", 18), fg="yellow", bg="black")
        self.category_label.pack(pady=10)

        self.frame = tk.Frame(self, bg="black")
        self.frame.pack()

        self.cells = []
        for r in range(ROWS):
            row_cells = []
            for c in range(COLS):
                lbl = tk.Label(self.frame, text="", font=("Arial Black", 24), width=3, height=2,
                               bg="gold", fg="black", borderwidth=2, relief="raised")
                lbl.grid(row=r, column=c, padx=2, pady=2)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        self.used_letters_label = tk.Label(self, text="Genutzte Buchstaben: ", font=("Arial Black", 16),
                                           fg="red", bg="blue")
        self.used_letters_label.pack(pady=10, fill="x")

    def start_server_thread(self):
        threading.Thread(target=self.socket_server, daemon=True).start()

    def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        continue
                    try:
                        msg = json.loads(data.decode('utf-8'))
                        puzzle = msg.get("puzzle")
                        category = msg.get("category", "")
                        if puzzle and len(puzzle) == ROWS and all(len(row) == COLS for row in puzzle):
                            self.puzzle = puzzle
                            self.category = category
                            self.revealed = [[False]*COLS for _ in range(ROWS)]
                            self.used_letters.clear()

                            # Alle Nicht-Buchstaben (keine A-Z) sofort aufdecken (inkl. Zahlen, Sonderzeichen, Umlaute)
                            for r in range(ROWS):
                                for c in range(COLS):
                                    ch = self.puzzle[r][c]
                                    # Leer = Feld nicht verwendet = grün
                                    if ch.strip() == "":
                                        continue
                                    # Wenn kein Großbuchstabe A-Ü, sofort aufgedeckt
                                    if not ("A" <= ch.upper() <= "Ü"):
                                        self.revealed[r][c] = True

                            self.update_display()

                    except Exception as e:
                        print("Fehler beim Verarbeiten:", e)

    def update_display(self):
        self.category_label.config(text=f"Kategorie: {self.category}")
        for r in range(ROWS):
            for c in range(COLS):
                ch = self.puzzle[r][c]
                if ch.strip() == "":  # Nicht verwendet
                    self.cells[r][c].config(text="", bg="gold")
                elif self.revealed[r][c]:  # Aufgedeckt
                    self.cells[r][c].config(text=ch.upper(), bg="white", fg="black")
                else:  # Nicht aufgedeckt
                    self.cells[r][c].config(text="", bg="gray")
        self.used_letters_label.config(text="Genutzte Buchstaben: " + ", ".join(sorted(self.used_letters)))
        self.update_idletasks()

    def on_key_press(self, event):
        key = event.char.upper()
        if len(key) != 1 or key == " ":
            return

        with self.lock:
            if self.is_uncovering or key in self.used_letters:
                return
            self.used_letters.add(key)

        threading.Thread(target=self.uncover_letters_with_sound, args=(key,), daemon=True).start()

    def uncover_letters_with_sound(self, key):
        with self.lock:
            self.is_uncovering = True

        positions = [(r, c) for r in range(ROWS) for c in range(COLS) if self.puzzle[r][c].upper() == key]

        if positions:
            for pos in positions:
                r, c = pos
                self.revealed[r][c] = True
                self.update_display()
                # Sound so oft abspielen, wie Buchstabe vorkommt
                if self.sound_buchstabe:
                    self.sound_buchstabe.play()
                time.sleep(0.3)
        else:
            if self.sound_kein_buchstabe:
                self.sound_kein_buchstabe.play()
            time.sleep(0.5)

        self.update_display()

        with self.lock:
            self.is_uncovering = False


if __name__ == "__main__":
    app = DisplayApp()
    app.mainloop()
