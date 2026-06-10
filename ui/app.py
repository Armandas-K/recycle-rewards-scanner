import tkinter as tk
from ui.screens.idle import IdleScreen
from ui.screens.welcome import WelcomeScreen
from ui.screens.scanning import ScanningScreen
from ui.screens.loading import LoadingScreen

class App:
    def __init__(self, root: tk.Tk, on_checkout=None, fullscreen: bool = True):
        self.root = root
        self.root.title("Recycle Rewards")

        if fullscreen:
            self.root.state("zoomed")
            #self.root.attributes("-fullscreen", True)
            #self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        else:
            self.root.geometry("1000x700")

        self._on_checkout = on_checkout

        self.idle = IdleScreen(root, app=self)
        self.welcome = WelcomeScreen(root, app=self)
        self.scanning = ScanningScreen(root, app=self)
        self.loading = LoadingScreen(root, app=self)

        self._current = None
        self.show(self.idle)

    def show(self, screen):
        if self._current and hasattr(self._current, "on_hide"):
            self._current.on_hide()
        for s in [self.idle, self.welcome, self.scanning, self.loading]:
            s.pack_forget()
        screen.pack(fill=tk.BOTH, expand=True)
        if hasattr(screen, "on_show"):
            screen.on_show()
        self._current = screen

    def _set_language(self, language: str):
        for screen in [self.welcome, self.scanning, self.loading]:
            screen.set_language(language)

    def go_idle(self):
        self._set_language("en")
        self.show(self.idle)

    def go_welcome(self, name: str, language: str = "en"):
        self._set_language(language)
        self.welcome.set_user(name)
        self.show(self.welcome)

    def go_scanning(self):
        self.show(self.scanning)

    def go_loading(self):
        self.show(self.loading)
        if self._on_checkout:
            self._on_checkout()