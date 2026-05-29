import tkinter as tk
from core.camera import CameraFeed
from core.scanner import BarcodeScanner
from utils.barcode_lookup import is_in_cache, lookup

def on_scan(barcode):
    if is_in_cache(barcode):
        print(f"Valid container: {barcode}")
        # TODO: generate QR code for user to scan
        return

    # not in local cache - fall back to API
    result = lookup(barcode)
    if result["found"] and not result["flagged"]:
        print(f"Valid via API: {result['name']}")
        # TODO: generate QR code for user to scan
        return

    # TODO: show rejection in ui
    print(f"Invalid Barcode")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Recycle Rewards")
    # TODO: build full UI here

    scanner = BarcodeScanner(on_scan=on_scan)
    # source = webcam
    feed = CameraFeed(root, source=0, on_frame=scanner.process_frame)
    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()