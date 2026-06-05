import tkinter as tk
from ui.screens.idle import IdleScreen
from ui.screens.welcome import WelcomeScreen
from ui.screens.scanning import ScanningScreen
from ui.screens.loading import LoadingScreen
from ui.screens.qr_screen import QRScreen


class App:
    def __init__(self, root: tk.Tk, on_checkout=None, fullscreen: bool = True):
        self.root = root
        self.root.title("Recycle Rewards")

        if fullscreen:
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        else:
            self.root.geometry("1000x700")

        self._on_checkout = on_checkout

        self.idle = IdleScreen(root, app=self)
        self.welcome = WelcomeScreen(root, app=self)
        self.scanning = ScanningScreen(root, app=self)
        self.loading = LoadingScreen(root, app=self)
        self.qr = QRScreen(root, app=self)

        self._current = None
        self.show(self.idle)

    def show(self, screen):
        if self._current and hasattr(self._current, "on_hide"):
            self._current.on_hide()
        for s in [self.idle, self.welcome, self.scanning, self.loading, self.qr]:
            s.pack_forget()
        screen.pack(fill=tk.BOTH, expand=True)
        if hasattr(screen, "on_show"):
            screen.on_show()
        self._current = screen

    def go_idle(self):
        self.show(self.idle)

    def go_welcome(self, name: str):
        self.welcome.set_user(name)
        self.show(self.welcome)
    # legacy
    def go_scanning(self):
        self.show(self.scanning)

    def go_loading(self):
        self.show(self.loading)
        if self._on_checkout:
            self._on_checkout()
    # legacy
    def go_qr(self, qr_data: str):
        self.qr.set_qr(qr_data)
        self.show(self.qr)