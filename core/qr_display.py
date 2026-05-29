import qrcode
import tkinter as tk
from PIL import ImageTk

class QRDisplay:
    def __init__(self, parent: tk.Widget, size: int = 300):
        self.size = size
        self.frame = tk.Frame(parent, bg="white")
        self.label = tk.Label(self.frame, bg="white")
        self.label.pack(padx=20, pady=20)
        self._img_ref = None

    def show(self, data: str):
        # generate and display qr code for given string
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((self.size, self.size))

        self._img_ref = ImageTk.PhotoImage(img)
        self.label.configure(image=self._img_ref)
        self.frame.pack()

    def hide(self):
        # hide qr code display
        self.frame.pack_forget()
        self._img_ref = None