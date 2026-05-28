import tkinter as tk
from camera import CameraFeed
from scanner import BarcodeScanner
from utils.barcode_lookup import is_in_cache, lookup

# camera stream url, must be on same wi-fi
# using "IP Webcam" on playstore
STREAM_URL = "http://192.168.1.196:8080/video"

def on_scan(barcode):
    print(f"\n[DEBUG] Barcode: {barcode}")

    in_cache = is_in_cache(barcode)
    print(f"[DEBUG] Cache hit: {in_cache}")

    result = lookup(barcode)

    if result["found"]:
        print(f"[DEBUG] Product: {result['name']}")
        print(f"[DEBUG] Category: {result['category']}")
        print(f"[DEBUG] Flagged: {result['flagged']}")
    else:
        print(f"[DEBUG] Not in Open Food Facts - flagged for review")

if __name__ == "__main__":
    root = tk.Tk()
    scanner = BarcodeScanner(on_scan=on_scan)
    feed = CameraFeed(root, source=STREAM_URL, on_frame=scanner.process_frame)
    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()