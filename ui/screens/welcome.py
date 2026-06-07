import tkinter as tk
from ui.style import *
from utils.translations import get_text

class WelcomeScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._name = ""
        self._language = "en"
        self._build()

    def _build(self):
        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._greeting = tk.Label(center, text="", font=FONT_HEADING, bg=BG, fg=TEXT)
        self._greeting.pack()

        self._subtitle = tk.Label(center, text="", font=FONT_LABEL, bg=BG, fg=TEXT_DIM)
        self._subtitle.pack(pady=(20, 0))

    def _update_text(self):
        greeting_fmt = get_text(self._language, "welcome", "greeting")
        self._greeting.configure(text=greeting_fmt.format(name=self._name))
        self._subtitle.configure(text=get_text(self._language, "welcome", "subtitle"))

    def set_user(self, name: str):
        self._name = name
        self._update_text()

    def set_language(self, language: str):
        self._language = language
        self._update_text()

    def on_show(self):
        pass