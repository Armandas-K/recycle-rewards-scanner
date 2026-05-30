import tkinter as tk
from ui.style import *

class LoadingScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._dot_count = 0
        self._after_job = None
        self._build()

    def _build(self):
        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._heading = tk.Label(center, text="Processing", font=FONT_HEADING, bg=BG, fg=TEXT)
        self._heading.pack()

        tk.Label(center, text="Please wait", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack(pady=(10, 0))

    def _animate(self):
        self._dot_count = (self._dot_count + 1) % 4
        self._heading.configure(text=f"Processing{'.' * self._dot_count}")
        self._after_job = self.after(500, self._animate)

    def on_show(self):
        self._dot_count = 0
        self._animate()

    def on_hide(self):
        if self._after_job:
            self.after_cancel(self._after_job)
            self._after_job = None