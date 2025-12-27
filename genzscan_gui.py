import tkinter as tk
from tkinter import messagebox # type: ignore
from scanner.core import run_scan  # type: ignore
# ... (buat window dengan entry URL, button scan, text output neon style)
# Contoh dasar:
root = tk.Tk()
root.title("GEN Z SCAN GUI")
# Tambah label banner ASCII di text widget
# Button "Scan" call run_scan & show issues in listbox
root.mainloop()