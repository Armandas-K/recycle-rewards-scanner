import tkinter as tk
from ui.style import *
from utils.translations import get_text

class LoadingScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._dot_count = 0
        self._after_job = None
        self._base_heading = get_text("en", "loading", "heading")
        self._build()

    def _build(self):
        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._heading = tk.Label(center, text="", font=FONT_HEADING, bg=BG, fg=TEXT)
        self._heading.pack()

        self._subtitle = tk.Label(center, text="", font=FONT_LABEL, bg=BG, fg=TEXT_DIM)
        self._subtitle.pack(pady=(10, 0))

        self.set_language("en")

    def set_language(self, language: str):
        self._base_heading = get_text(language, "loading", "heading")
        self._subtitle.configure(text=get_text(language, "loading", "subtitle"))

    def _animate(self):
        self._dot_count = (self._dot_count + 1) % 4
        self._heading.configure(text=f"{self._base_heading}{'.' * self._dot_count}")
        self._after_job = self.after(500, self._animate)

    def on_show(self):
        self._dot_count = 0
        self._animate()

    def on_hide(self):
        if self._after_job:
            self.after_cancel(self._after_job)
            self._after_job = None