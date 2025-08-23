import tkinter as tk
import threading
import socket
import json
import time
import pygame
import os

ROWS, COLS = 4, 13
HOST = "0.0.0.0"
PORT = 65432
SOUND_PATH = r"C:\Users\andre\Desktop\Neuer Ordner (3)\000\ratewand\sounds"

VOWELS = {"A", "E", "I", "O", "U", "Ä", "Ö", "Ü"}

class DisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ratewand Display")
        self.configure(bg="#000000")

        pygame.mixer.init()
        self.sound_buchstabe = self.load_sound("buchstabe.mp3")
        self.sound_kein_buchstabe = self.load_sound("kein_buchstabe.mp3")
        self.sound_new_puzzle = self.load_sound("new_puzzle.mp3")
        self.sound_keine_kons = self.load_sound("keinekons.mp3")
        self.sound_geloest = self.load_sound("geloest.mp3")
        self.sound_bonus = self.load_sound("bonus.mp3")
        self.sound_bonus_loes = self.load_sound("bonus_loes.mp3")

        self.puzzle = [["" for _ in range(COLS)] for _ in range(ROWS)]
        self.revealed = [[False]*COLS for _ in range(ROWS)]
        self.used_letters = set()
        self.category = ""

        self.bonus_running = False
        self.bonus_countdown = 0

        self.create_widgets()
        self.start_server_thread()
        self.bind("<Key>", self.on_key_press)

        self.lock = threading.Lock()
        self.is_uncovering = False

        self.led_state = False
        self.after(500, self.toggle_leds)

    # ---------------- Sounds ----------------
    def load_sound(self, filename):
        try:
            return pygame.mixer.Sound(os.path.join(SOUND_PATH, filename))
        except Exception as e:
            print(f"Fehler beim Laden von {filename}:", e)
            return None

    def play_sound(self, sound, loops=0):
        if sound:
            sound.play(loops=loops)

    def stop_sound(self, sound):
        if sound:
            sound.stop()

    # ---------------- Widgets ----------------
    def create_widgets(self):
        self.category_label = tk.Label(self, text="Kategorie: ", font=("Arial Black", 18), fg="yellow", bg="black")
        self.category_label.pack(pady=10)

        self.led_frame = tk.Frame(self, bg="black")
        self.led_frame.pack()

        self.leds_top = [tk.Label(self.led_frame, width=2, height=1, bg="darkred") for _ in range(COLS)]
        self.leds_bottom = [tk.Label(self.led_frame, width=2, height=1, bg="darkred") for _ in range(COLS)]
        self.leds_left = [tk.Label(self.led_frame, width=2, height=1, bg="darkred") for _ in range(ROWS)]
        self.leds_right = [tk.Label(self.led_frame, width=2, height=1, bg="darkred") for _ in range(ROWS)]

        for i, led in enumerate(self.leds_top):
            led.grid(row=0, column=i+1, padx=1, pady=1)
        for i, led in enumerate(self.leds_bottom):
            led.grid(row=ROWS+1, column=i+1, padx=1, pady=1)
        for i, led in enumerate(self.leds_left):
            led.grid(row=i+1, column=0, padx=1, pady=1)
        for i, led in enumerate(self.leds_right):
            led.grid(row=i+1, column=COLS+1, padx=1, pady=1)

        self.cells = []
        for r in range(ROWS):
            row_cells = []
            for c in range(COLS):
                lbl = tk.Label(self.led_frame, text="", font=("Arial Black", 24), width=3, height=2,
                               bg="gold", fg="black", borderwidth=2, relief="raised")
                lbl.grid(row=r+1, column=c+1, padx=2, pady=2)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        self.used_letters_label = tk.Label(self, text="Genutzte Buchstaben: ", font=("Arial Black", 16),
                                           fg="red", bg="blue")
        self.used_letters_label.pack(pady=10, fill="x")

        self.bonus_label = tk.Label(self, text="", font=("Arial Black", 16), fg="yellow", bg="black")
        self.bonus_label.pack(pady=5)

    # ---------------- LEDs ----------------
    def toggle_leds(self):
        self.led_state = not self.led_state
        on_color = "#FFD700"
        off_color = "#B8860B"
        for idx, led in enumerate(self.leds_top + self.leds_bottom + self.leds_left + self.leds_right):
            if idx % 2 == (0 if self.led_state else 1):
                led.config(bg=on_color)
            else:
                led.config(bg=off_color)
        self.after(500, self.toggle_leds)

    # ---------------- Server ----------------
    def start_server_thread(self):
        threading.Thread(target=self.socket_server, daemon=True).start()

    def socket_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        with conn:
            data = conn.recv(4096)
            if not data:
                return
            try:
                msg = json.loads(data.decode('utf-8'))

                # --- Steuerkommandos ---
                if "command" in msg:
                    if msg["command"] == "solved":
                        self.reveal_all()
                        self.play_sound(self.sound_geloest)
                    elif msg["command"] == "wrong":
                        self.play_sound(self.sound_kein_buchstabe)
                    elif msg["command"] == "bonus_show":
                        letters = msg.get("bonus_selected", [])
                        self.show_bonus_letters(letters)
                    elif msg["command"] == "bonus_start":
                        letters = msg.get("bonus_selected", [])
                        self.start_bonus(letters)
                    elif msg["command"] == "bonus_solved":
                        self.stop_sound(self.sound_bonus)
                        self.reveal_all()
                        self.play_sound(self.sound_geloest)
                    elif msg["command"] == "reset_display":
                        self.reset_display()
                    return

                # Normales Puzzle
                puzzle = msg.get("puzzle")
                category = msg.get("category", "")
                if puzzle and len(puzzle) == ROWS and all(len(row) == COLS for row in puzzle):
                    self.puzzle = puzzle
                    self.category = category
                    self.revealed = [[False]*COLS for _ in range(ROWS)]
                    self.used_letters.clear()
                    for r in range(ROWS):
                        for c in range(COLS):
                            ch = self.puzzle[r][c]
                            if ch.strip() == "":
                                continue
                            if not ("A" <= ch.upper() <= "Ü"):
                                self.revealed[r][c] = True
                    self.update_display()
                    self.play_sound(self.sound_new_puzzle)
            except Exception as e:
                print("Fehler beim Verarbeiten:", e)

    # ---------------- Anzeige ----------------
    def update_display(self):
        self.category_label.config(text=f"Kategorie: {self.category}")
        for r in range(ROWS):
            for c in range(COLS):
                ch = self.puzzle[r][c]
                if ch.strip() == "":
                    self.cells[r][c].config(text="", bg="gold")
                elif self.revealed[r][c]:
                    self.cells[r][c].config(text=ch.upper(), bg="white", fg="black")
                else:
                    self.cells[r][c].config(text="", bg="gray")
        self.used_letters_label.config(text="Genutzte Buchstaben: " + ", ".join(sorted(self.used_letters)))
        self.update_idletasks()

    # ---------------- Bonus Funktionen ----------------
    def show_bonus_letters(self, letters):
        if not letters:
            return
        # Enthüllt nur die Buchstaben, die im Rätsel vorhanden sind
        for key in letters:
            key = key.upper()
            self.used_letters.add(key)
            for r in range(ROWS):
                for c in range(COLS):
                    if self.puzzle[r][c].upper() == key:
                        self.revealed[r][c] = True
        self.update_display()

    def start_bonus(self, letters):
        if not letters:
            return
        self.show_bonus_letters(letters)
        self.bonus_running = True
        self.bonus_countdown = 10
        self.play_sound(self.sound_bonus, loops=-1)
        self.update_bonus_countdown_label()

    def update_bonus_countdown_label(self):
        if self.bonus_running and self.bonus_countdown >= 0:
            self.bonus_label.config(text=f"Bonusrunde Countdown: {self.bonus_countdown}")
            self.bonus_countdown -= 1
            self.after(1000, self.update_bonus_countdown_label)
        elif self.bonus_running:
            self.stop_sound(self.sound_bonus)
            self.bonus_label.config(text="Bonusrunde beendet")
            self.bonus_running = False

    # ---------------- Tastenevents ----------------
    def highlight_cell(self, r, c):
        original_bg = self.cells[r][c].cget("bg")
        self.cells[r][c].config(bg="lightgreen")
        self.after(200, lambda: self.cells[r][c].config(bg=original_bg))

    def on_key_press(self, event):
        key = event.char.upper()
        if len(key) != 1 or key == " ":
            return
        if key == "*":
            self.reveal_all()
            return
        with self.lock:
            if self.is_uncovering or key in self.used_letters:
                return
            self.used_letters.add(key)
        threading.Thread(target=self.uncover_letters_with_sound, args=(key,), daemon=True).start()

    def reveal_all(self):
        self.revealed = [[True]*COLS for _ in range(ROWS)]
        self.update_display()

    def uncover_letters_with_sound(self, key):
        with self.lock:
            self.is_uncovering = True
        positions = [(r, c) for r in range(ROWS) for c in range(COLS) if self.puzzle[r][c].upper() == key]
        if positions:
            for r, c in positions:
                self.revealed[r][c] = True
                self.update_display()
                self.highlight_cell(r, c)
                self.play_sound(self.sound_buchstabe)
                time.sleep(0.3)
            if key not in VOWELS and not self.any_consonants_left():
                self.play_sound(self.sound_keine_kons)
        else:
            self.play_sound(self.sound_kein_buchstabe)
            time.sleep(0.5)
        self.update_display()
        with self.lock:
            self.is_uncovering = False

    # ---------------- Helfer ----------------
    def any_consonants_left(self):
        for r in range(ROWS):
            for c in range(COLS):
                ch = self.puzzle[r][c].upper()
                if ch.strip() != "" and ch not in VOWELS and not self.revealed[r][c]:
                    return True
        return False

    # ---------------- Reset ----------------
    def reset_display(self):
        self.puzzle = [["" for _ in range(COLS)] for _ in range(ROWS)]
        self.revealed = [[False]*COLS for _ in range(ROWS)]
        self.used_letters.clear()
        self.category = ""
        self.bonus_running = False
        self.bonus_countdown = 0
        self.stop_sound(self.sound_bonus)
        self.update_display()
        self.bonus_label.config(text="")

if __name__ == "__main__":
    app = DisplayApp()
    app.mainloop()
