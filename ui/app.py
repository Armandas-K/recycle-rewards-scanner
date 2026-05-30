import tkinter as tk
from ui.screens.scanning import ScanningScreen
from ui.screens.loading import LoadingScreen
from ui.screens.qr_screen import QRScreen


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Recycle Rewards")
        self.root.attributes("-fullscreen", True)

        self.scanning = ScanningScreen(root, app=self)
        self.loading = LoadingScreen(root, app=self)
        self.qr = QRScreen(root, app=self)

        self.show(self.scanning)

    def show(self, screen):
        for s in [self.scanning, self.loading, self.qr]:
            s.pack_forget()
        screen.pack(fill=tk.BOTH, expand=True)

    def go_scanning(self):
        self.show(self.scanning)

    def go_loading(self):
        self.show(self.loading)

    def go_qr(self, qr_data: str):
        self.qr.set_qr(qr_data)
        self.show(self.qr)