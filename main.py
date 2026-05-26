import tkinter as tk
from camera import CameraFeed
from scanner import BarcodeScanner


def on_scan(barcode):
    print(f"Scanned: {barcode}")
    # TODO: validate against cache, generate QR for user


if __name__ == "__main__":
    root = tk.Tk()
    scanner = BarcodeScanner(on_scan=on_scan)
    # source = webcam
    feed = CameraFeed(root, source=0, on_frame=scanner.process_frame)
    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()