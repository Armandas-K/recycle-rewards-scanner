from pyzbar.pyzbar import decode
import time

class BarcodeScanner:
    def __init__(self, on_scan):
        self.on_scan = on_scan
        self.last_scan = ("", 0)
        self.cooldown = 3  # seconds before same barcode triggers again

    def process_frame(self, frame):
        barcodes = decode(frame)
        for barcode in barcodes:
            data = barcode.data.decode("utf-8")
            now = time.time()

            # ignore repeated scans of same barcode within cooldown
            if data == self.last_scan[0] and now - self.last_scan[1] < self.cooldown:
                continue

            self.last_scan = (data, now)
            self.on_scan(data)