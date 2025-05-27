import tkinter as tk
from tkinter import messagebox
import socket
import json

HOST = "127.0.0.1"
PORT = 65432

ROWS, COLS = 4, 13

class ControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ratewand Control")
        self.configure(bg="white")

        self.category_var = tk.StringVar()

        # Kategorie-Eingabe
        tk.Label(self, text="Kategorie:", font=("Arial Black", 16), bg="white").pack(pady=(10,0))
        self.category_entry = tk.Entry(self, font=("Arial", 14), textvariable=self.category_var)
        self.category_entry.pack(padx=10, pady=(0,10), fill="x")

        # Grid mit Eingabefeldern 4x13
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

        # Button zum Senden
        self.send_button = tk.Button(self, text="Änderungen senden", font=("Arial Black", 14), command=self.send_puzzle)
        self.send_button.pack(pady=(10,20))

        # Initiale Farben setzen
        self.update_colors()

    def on_key_release(self, event):
        # Ein Feld darf nur 1 Zeichen enthalten
        widget = event.widget
        txt = widget.get()
        if len(txt) > 1:
            widget.delete(1, tk.END)
        self.update_colors()

    def update_colors(self):
        for r in range(ROWS):
            for c in range(COLS):
                val = self.entries[r][c].get()
                # Grün: nicht verwendet (leer)
                # Weiß: Buchstabe, Ziffer, Satz-/Sonderzeichen (also alles außer leer)
                if val.strip() == "":
                    self.entries[r][c].config(bg="gold")
                else:
                    self.entries[r][c].config(bg="white")

    def send_puzzle(self):
        puzzle = []
        for r in range(ROWS):
            row_data = []
            for c in range(COLS):
                ch = self.entries[r][c].get()
                if ch == "":
                    ch = " "
                row_data.append(ch)
            puzzle.append(row_data)

        category = self.category_var.get()

        msg = {
            "category": category,
            "puzzle": puzzle
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(json.dumps(msg).encode("utf-8"))
        except ConnectionRefusedError:
            messagebox.showerror("Fehler", "Display-Programm ist nicht gestartet oder nicht erreichbar.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Senden:\n{e}")

if __name__ == "__main__":
    app = ControlApp()
    app.mainloop()
