import tkinter as tk
from ui.style import *

class IdleScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(center, text="♻", font=("Helvetica", 80), bg=BG, fg=ACCENT).pack()
        tk.Label(center, text="RECYCLE REWARDS", font=FONT_HEADING, bg=BG, fg=TEXT).pack(pady=(20, 0))
        tk.Label(
            center,
            text="Tap your phone or card to begin",
            font=FONT_LABEL,
            bg=BG,
            fg=TEXT_DIM
        ).pack(pady=(15, 0))

    def on_show(self):
        pass