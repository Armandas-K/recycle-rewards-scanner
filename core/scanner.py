from pyzbar.pyzbar import decode, ZBarSymbol
from utils.validator import is_valid_barcode
import time

class BarcodeScanner:
    def __init__(self, on_scan):
        self.on_scan = on_scan
        self.last_scan = ("", 0) # barcode, timestamp
        self.last_any_scan = 0 # timestamp only

        self.cooldown_same = 5 # seconds before same barcode triggers again
        self.cooldown_any = 2 # seconds before any barcode triggers again

    def process_frame(self, frame):
        barcodes = decode(frame, symbols=[ZBarSymbol.EAN13, ZBarSymbol.EAN8, ZBarSymbol.UPCA])
        for barcode in barcodes:
            data = barcode.data.decode("utf-8")

            valid, reason = is_valid_barcode(data)
            if not valid:
                print(f"[IGNORED] {data} - {reason}")
                continue

            now = time.time()

            if now - self.last_any_scan < self.cooldown_any:
                continue

            if data == self.last_scan[0] and now - self.last_scan[1] < self.cooldown_same:
                continue

            self.last_scan = (data, now)
            self.last_any_scan = now
            self.on_scan(data)