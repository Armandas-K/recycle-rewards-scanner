import tkinter as tk
from camera import CameraFeed
from scanner import BarcodeScanner

# camera stream url, must be on same wi-fi
# using "IP Webcam" on playstore
STREAM_URL = "http://192.168.1.196:8080/video"

def on_scan(barcode):
    print(f"[DEBUG] Barcode detected: {barcode}")
    print(f"[DEBUG] Length: {len(barcode)} chars")
    # TODO: print whether barcode is in cache


if __name__ == "__main__":
    root = tk.Tk()
    scanner = BarcodeScanner(on_scan=on_scan)
    feed = CameraFeed(root, source=STREAM_URL, on_frame=scanner.process_frame)
    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()