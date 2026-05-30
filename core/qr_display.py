from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
import tkinter as tk
from PIL import ImageTk

class QRDisplay:
    def __init__(self, parent: tk.Misc, size: int = 300):
        self.parent = parent
        self.size = size
        self._img_ref = None
        self._window = None
        self._label = None

    def _init_window(self):
        self._window = tk.Toplevel(self.parent)
        self._window.title("Scan to claim points")
        self._window.protocol("WM_DELETE_WINDOW", self.hide)
        self._label = tk.Label(self._window, bg="white")
        self._label.pack(padx=20, pady=20)

    def show(self, data: str):
        # generate and display qr code for given string
        if self._window is None:
            self._init_window()
        else:
            self._window.deiconify()

        qr = QRCode(
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((self.size, self.size))

        self._img_ref = ImageTk.PhotoImage(img)
        self._label.configure(image=self._img_ref)

    def hide(self):
        self._img_ref = None
        if self._window:
            self._window.withdraw()