import tkinter as tk
import queue
import threading

from ui.app import App
from api.session import ScanSession
from api.client import get_user, checkout
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
INACTIVITY_TIMEOUT = 30_000  # ms - checkout triggered after no scan for 30 seconds

session = ScanSession()
_inactivity_job  = None

# Inactivity timer

def reset_inactivity_timer():
    global _inactivity_job
    if _inactivity_job:
        root.after_cancel(_inactivity_job)
    _inactivity_job = root.after(INACTIVITY_TIMEOUT, _on_inactivity)

def cancel_inactivity_timer():
    global _inactivity_job
    if _inactivity_job:
        root.after_cancel(_inactivity_job)
        _inactivity_job = None

def _on_inactivity():
    global _inactivity_job
    _inactivity_job = None
    if session.active:
        print("[INACTIVITY] No scan for 30 seconds - checking out")
        app.go_loading()

# NFC event handler (main thread)

def on_nfc_tap(uid: str):
    if not session.active:
        # first tap
        user = get_user(uid)
        if not user.get("found"):
            print(f"[NFC] User not found for UID: {uid} - using defaults")
        session.start(uid, user)
        reset_inactivity_timer()
        app.go_welcome(user.get("name", "User"))

    elif uid == session.uid:
        # same user taps again - checkout
        app.go_loading()

    else:
        # different user - checkout current then welcome new
        on_checkout()
        user = get_user(uid)
        if not user.get("found"):
            print(f"[NFC] User not found for UID: {uid} - using defaults")
        session.start(uid, user)
        reset_inactivity_timer()
        app.go_welcome(user.get("name", "User"))

def poll_nfc():
    try:
        uid = nfc_queue.get_nowait()
        on_nfc_tap(uid)
    except queue.Empty:
        pass
    root.after(100, poll_nfc)

def console_nfc_input():
    # type a uid in the console to simulate an nfc tap (for easier testing)
    while True:
        uid = input().strip()
        if uid:
            nfc_queue.put(uid)

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
        reset_inactivity_timer()

        if app._current == app.welcome:
            app.go_scanning()

        app.scanning.update_count(session.count)
        app.scanning.update_points(session.count * POINTS_PER_BOTTLE)

def on_checkout():
    cancel_inactivity_timer()

    bottles = session.count
    points = bottles * POINTS_PER_BOTTLE
    uid = session.uid
    name = session.user.get("name")

    print(f"[CHECKOUT] {bottles} bottle(s), {points} points for {name} ({uid})")

    if bottles > 0:
        result = checkout(uid, bottles, points)
        if result.get("success"):
            print(f"[CHECKOUT] Success")
        else:
            print(f"[CHECKOUT] Failed or backend not available")

    session.clear()
    root.after(2000, app.go_idle)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, on_checkout=on_checkout, fullscreen=False)

    camera_window = tk.Toplevel(root)
    camera_window.title("Camera Feed Debug")

    # position feed in top-right corner
    screen_w = root.winfo_screenwidth()
    camera_window.geometry(f"+{screen_w - 400}+0")

    # nfc tap thread
    start_nfc()
    # console input nfc thread
    threading.Thread(target=console_nfc_input, daemon=True).start()

    scanner = BarcodeScanner(on_scan=on_scan)
    feed = CameraFeed(camera_window, source=CAMERA_SOURCE, on_frame=scanner.process_frame, display=True, display_scale=0.35)

    root.after(100, poll_nfc)

    root.protocol("WM_DELETE_WINDOW", lambda: (feed.release(), root.destroy()))
    root.mainloop()