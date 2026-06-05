class ScanSession:
    def __init__(self):
        self._barcodes: list[str] = []
        self.uid: str | None = None
        self.user: dict = {}

    def start(self, uid: str, user: dict):
        self._barcodes.clear()
        self.uid  = uid
        self.user = user
        print(f"[SESSION] Started for {user.get('name', 'Unknown')} ({uid})")

    def add(self, barcode: str):
        self._barcodes.append(barcode)
        print(f"[SESSION] Added {barcode} - {self.count} item(s) in session")

    def checkout(self) -> list[str]:
        items = self._barcodes.copy()
        self._barcodes.clear()
        return items

    def clear(self):
        self._barcodes.clear()
        self.uid  = None
        self.user = {}

    @property
    def count(self) -> int:
        return len(self._barcodes)

    @property
    def active(self) -> bool:
        return self.uid is not None