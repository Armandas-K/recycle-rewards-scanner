import tkinter as tk
from core.camera import CameraFeed
from core.scanner import BarcodeScanner
from ui.app import App
from api.session import ScanSession
from utils.barcode_lookup import is_in_cache, lookup

# camera stream url, must be on same wi-fi
# using "IP Webcam" on playstore
STREAM_URL = "http://192.168.1.196:8080/video"
POINTS_PER_BOTTLE = 5

session = ScanSession()

def on_scan(barcode):
    print(f"\n[DEBUG] Barcode: {barcode}")

    in_cache = is_in_cache(barcode)
    print(f"[DEBUG] Cache hit: {in_cache}")

    result = lookup(barcode)
    if result["found"]:
        print(f"[DEBUG] Product: {result['name']}")
        print(f"[DEBUG] Category: {result['category']}")
    else:
        print(f"[DEBUG] Not in Open Food Facts - flagged for review")

    if in_cache or result["found"]:
        session.add(barcode)
        if app:
            app.scanning.update_count(session.count())
            app.scanning.update_points(session.count() * POINTS_PER_BOTTLE)


def on_checkout():
    barcodes = session.checkout()
    print(f"\n[DEBUG] Checkout - {len(barcodes)} bottle(s): {barcodes}")

    if app:
        app.scanning.update_count(0)
        app.scanning.update_points(0)

    # simulate API delay
    if root:
        root.after(2000, lambda: app.go_qr("example.redeem"))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, on_checkout=on_checkout)

    camera_window = tk.Toplevel(root)
    camera_window.title("Camera Feed Debug")

    scanner = BarcodeScanner(on_scan=on_scan)
    feed = CameraFeed(camera_window, source=STREAM_URL, on_frame=scanner.process_frame, display=True)

    # make ui frame in focus so esc works
    root.lift()
    root.focus_force()

    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()