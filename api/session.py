class ScanSession:
    def __init__(self):
        self._bottles: list[str] = []
        self._cans: list[str] = []
        self.uid: str | None = None
        self.user: dict = {}

    def start(self, uid: str, user: dict):
        self._bottles.clear()
        self._cans.clear()
        self.uid = uid
        self.user = user
        print(f"[SESSION] Started for {user.get('name', 'Unknown')} ({uid})")

    def add(self, barcode: str, container_type: str):
        if container_type == "can":
            self._cans.append(barcode)
        else:
            self._bottles.append(barcode)
        print(f"[SESSION] Added {container_type} {barcode} - {self.bottle_count} bottle(s), {self.can_count} can(s)")

    def checkout(self) -> tuple[list[str], list[str]]:
        bottles = self._bottles.copy()
        cans = self._cans.copy()
        self._bottles.clear()
        self._cans.clear()
        return bottles, cans

    def clear(self):
        self._bottles.clear()
        self._cans.clear()
        self.uid  = None
        self.user = {}

    @property
    def bottle_count(self) -> int:
        return len(self._bottles)

    @property
    def can_count(self) -> int:
        return len(self._cans)

    @property
    def count(self) -> int:
        return self.bottle_count + self.can_count

    @property
    def active(self) -> bool:
        return self.uid is not None