import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import json
import os

HOSTS = ["127.0.0.1", "127.0.0.1"]
PORT = 65432

ROWS, COLS = 4, 13
PUZZLE_FILE = "puzzles.json"

class ControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ratewand Control")
        self.configure(bg="white")

        self.category_var = tk.StringVar()
        self.bonus_var = tk.BooleanVar()
        self.bonus_letters = []

        # Kategorie
        tk.Label(self, text="Kategorie:", font=("Arial Black", 16), bg="white").pack(pady=(10,0))
        self.category_entry = tk.Entry(self, font=("Arial", 14), textvariable=self.category_var)
        self.category_entry.pack(padx=10, pady=(0,10), fill="x")

        # Grid 4x13
        self.entries = []
        frame = tk.Frame(self, bg="white")
        frame.pack(padx=10, pady=10)

        for r in range(ROWS):
            row_entries = []
            for c in range(COLS):
                e = tk.Entry(frame, font=("Arial Black", 20), width=2, justify="center",
                             bg="gold", fg="black", relief="solid", borderwidth=2)
                e.grid(row=r, column=c, padx=3, pady=3)
                e.bind("<KeyRelease>", self.on_key_release)
                row_entries.append(e)
            self.entries.append(row_entries)

        # Buttons
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=(10,20))

        tk.Button(button_frame, text="Änderungen senden", font=("Arial Black", 14),
                  command=self.send_puzzle).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Puzzle speichern", font=("Arial Black", 14),
                  command=self.save_puzzle).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Puzzle laden", font=("Arial Black", 14),
                  command=self.load_puzzle).grid(row=0, column=2, padx=5)

        # ---------------- Puzzle-Auswahl ----------------
        list_frame = tk.Frame(self, bg="white")
        list_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(list_frame, text="Gespeicherte Puzzles:", font=("Arial Black", 14), bg="white").pack(anchor="w")
        self.puzzle_listbox = tk.Listbox(list_frame, height=6, font=("Arial", 12))
        self.puzzle_listbox.pack(fill="x")
        self.puzzle_listbox.bind("<Double-Button-1>", self.on_puzzle_double_click)

        tk.Button(list_frame, text="Puzzle löschen", font=("Arial Black", 12),
                  command=self.delete_selected_puzzle).pack(pady=(5,0))
        tk.Button(list_frame, text="Puzzle bearbeiten", font=("Arial Black", 12),
                  command=self.edit_selected_puzzle).pack(pady=(5,0))

        # ---------------- Bonus Option ----------------
        bonus_frame = tk.Frame(self, bg="white")
        bonus_frame.pack(padx=10, pady=10, fill="x")
        tk.Checkbutton(bonus_frame, text="Bonusrunde aktivieren", font=("Arial Black", 12),
                       variable=self.bonus_var, bg="white").pack(anchor="w")

        self.update_puzzle_list()
        self.update_colors()

        # ---------------- Control-Buttons ----------------
        control_frame = tk.Frame(self, bg="white")
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Rätsel gelöst", font=("Arial Black", 12), command=self.solved).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Lösung falsch", font=("Arial Black", 12), command=self.wrong).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Bonus Buchstaben eingeben und anzeigen", font=("Arial Black", 12), command=self.show_bonus_letters).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(control_frame, text="Start Bonusrunde", font=("Arial Black", 12), command=self.start_bonus).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(control_frame, text="Bonus gelöst", font=("Arial Black", 12), command=self.bonus_solved).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(control_frame, text="Reset Display", font=("Arial Black", 12), command=self.reset_display).grid(row=3, column=0, columnspan=2, pady=5)

    # ---------------- Key-Event & Farben ----------------
    def on_key_release(self, event):
        widget = event.widget
        txt = widget.get()
        if len(txt) > 1:
            widget.delete(1, tk.END)
        self.update_colors()

    def update_colors(self):
        for r in range(ROWS):
            for c in range(COLS):
                val = self.entries[r][c].get()
                self.entries[r][c].config(bg="gold" if val.strip() == "" else "white")

    def get_current_puzzle(self):
        puzzle = []
        for r in range(ROWS):
            row_data = []
            for c in range(COLS):
                ch = self.entries[r][c].get() or " "
                row_data.append(ch)
            puzzle.append(row_data)
        category = self.category_var.get()
        return {"category": category, "puzzle": puzzle, "bonus_active": self.bonus_var.get(), "bonus_selected": self.bonus_letters}

    # ---------------- Senden ----------------
    def send_puzzle(self):
        msg = self.get_current_puzzle()
        for host in HOSTS:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, PORT))
                    s.sendall(json.dumps(msg).encode("utf-8"))
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Senden an {host}:\n{e}")

    # ---------------- Puzzle speichern / laden ----------------
    def save_puzzle(self):
        msg = self.get_current_puzzle()
        name = simpledialog.askstring("Puzzle speichern", "Name des Puzzles:")
        if not name:
            return
        puzzles = {}
        if os.path.exists(PUZZLE_FILE):
            with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
                puzzles = json.load(f)
        new_id = f"{max([int(k) for k in puzzles.keys()]+[0])+1:02d}"
        puzzles[new_id] = {"name": name, "category": msg["category"], "puzzle": msg["puzzle"]}
        with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
            json.dump(puzzles, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Gespeichert", f"Puzzle '{name}' mit ID {new_id} gespeichert.")
        self.update_puzzle_list()

    def load_puzzle(self):
        if not os.path.exists(PUZZLE_FILE):
            messagebox.showwarning("Fehler", "Keine gespeicherten Puzzles gefunden.")
            return
        with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
            puzzles = json.load(f)
        pid = simpledialog.askstring("Puzzle laden", "Gib die Puzzle-ID ein (z. B. 01):")
        if not pid or pid not in puzzles:
            messagebox.showerror("Fehler", f"Puzzle mit ID '{pid}' nicht gefunden.")
            return
        self.load_puzzle_into_grid(puzzles[pid])

    def update_puzzle_list(self):
        self.puzzle_listbox.delete(0, tk.END)
        if os.path.exists(PUZZLE_FILE):
            with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
                puzzles = json.load(f)
            for pid, data in puzzles.items():
                display_text = f"{pid} - {data.get('name','')} ({data.get('category','')})"
                self.puzzle_listbox.insert(tk.END, display_text)

    def on_puzzle_double_click(self, event):
        selection = self.puzzle_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if os.path.exists(PUZZLE_FILE):
            with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
                puzzles = json.load(f)
            pid = list(puzzles.keys())[index]
            self.load_puzzle_into_grid(puzzles[pid])

    def load_puzzle_into_grid(self, data):
        self.category_var.set(data.get("category", ""))
        for r in range(ROWS):
            for c in range(COLS):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, data["puzzle"][r][c])
        self.update_colors()

    def delete_selected_puzzle(self):
        selection = self.puzzle_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if os.path.exists(PUZZLE_FILE):
            with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
                puzzles = json.load(f)
            pid = list(puzzles.keys())[index]
            if messagebox.askyesno("Löschen bestätigen", f"Willst du das Puzzle '{pid}' wirklich löschen?"):
                puzzles.pop(pid)
                with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
                    json.dump(puzzles, f, ensure_ascii=False, indent=2)
                self.update_puzzle_list()

    def edit_selected_puzzle(self):
        selection = self.puzzle_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if os.path.exists(PUZZLE_FILE):
            with open(PUZZLE_FILE, "r", encoding="utf-8") as f:
                puzzles = json.load(f)
            pid = list(puzzles.keys())[index]
            data = puzzles[pid]
            new_name = simpledialog.askstring("Puzzle bearbeiten", "Neuer Name:", initialvalue=data.get("name",""))
            if not new_name:
                return
            self.load_puzzle_into_grid(data)
            self.category_var.set(data.get("category",""))
            if messagebox.askyesno("Änderungen speichern", "Willst du die Änderungen speichern?"):
                updated_puzzle = self.get_current_puzzle()
                puzzles[pid] = {"name": new_name, "category": updated_puzzle["category"], "puzzle": updated_puzzle["puzzle"]}
                with open(PUZZLE_FILE, "w", encoding="utf-8") as f:
                    json.dump(puzzles, f, ensure_ascii=False, indent=2)
                self.update_puzzle_list()

    # ---------------- Control Buttons ----------------
    def solved(self):
        self.send_command("solved")

    def wrong(self):
        self.send_command("wrong")

    def show_bonus_letters(self):
        if not self.bonus_var.get():
            messagebox.showinfo("Info", "Bonusrunde nicht aktiviert!")
            return
        letters = simpledialog.askstring("Bonusbuchstaben", "Gib 5 Konsonanten + 1 Vokal ein (z.B. B C D F G A):")
        if letters:
            self.bonus_letters = letters.upper().split()
            self.send_command("bonus_show", self.bonus_letters)

    def start_bonus(self):
        if not self.bonus_var.get() or not self.bonus_letters:
            messagebox.showinfo("Info", "Bonusrunde oder Buchstaben fehlen!")
            return
        self.send_command("bonus_start", self.bonus_letters)

    def bonus_solved(self):
        self.send_command("bonus_solved", self.bonus_letters)

    def reset_display(self):
        self.send_command("reset_display")
        # Leere auch die Eingabefelder in der Control
        self.category_var.set("")
        self.bonus_letters = []
        for r in range(ROWS):
            for c in range(COLS):
                self.entries[r][c].delete(0, tk.END)
        self.update_colors()

    def send_command(self, cmd, bonus_selected=[]):
        msg = {"command": cmd, "bonus_selected": bonus_selected}
        for host in HOSTS:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, PORT))
                    s.sendall(json.dumps(msg).encode("utf-8"))
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Senden an {host}:\n{e}")

if __name__ == "__main__":
    app = ControlApp()
    app.mainloop()
