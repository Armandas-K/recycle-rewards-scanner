import tkinter as tk
from ui.style import *

class WelcomeScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._after_job = None
        self._build()

    def _build(self):
        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._greeting = tk.Label(center, text="", font=FONT_HEADING, bg=BG, fg=TEXT)
        self._greeting.pack()

        tk.Label(
            center,
            text="Start scanning bottles and cans to earn points",
            font=FONT_LABEL,
            bg=BG,
            fg=TEXT_DIM
        ).pack(pady=(20, 0))

    def set_user(self, name: str):
        self._greeting.configure(text=f"Hello, {name}")

    def on_show(self):
        self._after_job = self.after(2000, self.app.go_scanning)

    def on_hide(self):
        if self._after_job:
            self.after_cancel(self._after_job)
            self._after_job = None