class ScanSession:
    def __init__(self):
        self._barcodes: list[str] = []

    def add(self, barcode: str):
        self._barcodes.append(barcode)
        print(f"[SESSION] Added {barcode} - {len(self._barcodes)} item(s) in session")

    def checkout(self) -> list[str]:
        items = self._barcodes.copy()
        self._barcodes.clear()
        return items

    def clear(self):
        self._barcodes.clear()

    def count(self) -> int:
        return len(self._barcodes)