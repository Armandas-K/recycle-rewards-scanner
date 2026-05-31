import tkinter as tk
from PIL import ImageTk
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from ui.style import *

class QRScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._img_ref = None
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="SCAN QR CODE FOR POINTS\nOR PRINT VOUCHER",
            font=FONT_HEADING,
            bg=BG, fg=TEXT
        ).pack(pady=(60, 0))

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True)

        self._qr_label = tk.Label(center, bg=BG)
        self._qr_label.pack()

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(pady=40)

        tk.Button(
            bottom,
            text="GET VOUCHER",
            font=FONT_BUTTON,
            bg=ACCENT,
            fg=BTN_TEXT,
            padx=20, pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._on_voucher
        ).pack()

    def set_qr(self, data: str):
        qr = QRCode(error_correction=ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((300, 300))

        self._img_ref = ImageTk.PhotoImage(img)
        self._qr_label.configure(image=self._img_ref)

    def _on_voucher(self):
        # TODO: maybe show picture of voucher that would be printed?
        pass

    def on_show(self):
        pass