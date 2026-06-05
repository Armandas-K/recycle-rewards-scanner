import tkinter as tk
import queue

from ui.app import App
from api.session import ScanSession
from api.client import get_user
from core.camera import CameraFeed
from core.scanner import BarcodeScanner
from utils.barcode_lookup import is_in_cache, lookup
from utils.nfc_reader import nfc_queue, start as start_nfc

# camera stream url, must be on same wi-fi
# using "IP Webcam" on playstore
STREAM_URL = "http://192.168.1.196:8080/video"

# set to 0 for webcam, change index if wrong camera is selected
CAMERA_SOURCE = STREAM_URL
#CAMERA_SOURCE = 0

POINTS_PER_BOTTLE = 5

session = ScanSession()

# NFC event handler (main thread)

def on_nfc_tap(uid: str):
    if not session.active:
        user = get_user(uid)
        session.start(uid, user)
        app.go_welcome(user.get("name", "User"))

    elif uid == session.uid:
        # same user taps again - checkout
        on_checkout()

    else:
        # different user - checkout current then welcome new
        on_checkout()
        user = get_user(uid)
        session.start(uid, user)
        app.go_welcome(user.get("name", "User"))

def poll_nfc():
    try:
        uid = nfc_queue.get_nowait()
        on_nfc_tap(uid)
    except queue.Empty:
        pass
    root.after(100, poll_nfc)

# Scanning

def on_scan(barcode):
    if not session.active:
        return

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
        app.scanning.update_count(session.count)
        app.scanning.update_points(session.count * POINTS_PER_BOTTLE)

def on_checkout():
    bottles = session.count
    points = bottles * POINTS_PER_BOTTLE
    uid = session.uid
    name = session.user.get("name")

    print(f"[CHECKOUT] {bottles} bottle(s), {points} points for {name} ({uid})")

    # TODO: replace with real API call once backend is ready
    # checkout(uid, bottles, points)

    session.clear()
    app.go_loading()
    root.after(2000, app.go_idle)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, on_checkout=on_checkout, fullscreen=False)

    camera_window = tk.Toplevel(root)
    camera_window.title("Camera Feed Debug")

    # position feed in top-right corner
    screen_w = root.winfo_screenwidth()
    camera_window.geometry(f"+{screen_w - 400}+0")

    start_nfc()

    scanner = BarcodeScanner(on_scan=on_scan)
    feed = CameraFeed(camera_window, source=CAMERA_SOURCE, on_frame=scanner.process_frame, display=True, display_scale=0.35)

    root.after(100, poll_nfc)

    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()