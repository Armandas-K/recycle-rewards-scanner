import threading
import time
from api.client import get_transaction_status

class RedeemPoller:
    def __init__(self, root, token: str, on_redeemed, interval_s: int = 2):
        self.root = root
        self.token = token
        self.on_redeemed = on_redeemed
        self.interval_s = interval_s
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        print(f"[POLLER] Watching token {self.token}")

    def stop(self):
        self._running = False

    def _poll(self):
        while self._running:
            status = get_transaction_status(self.token)
            print(f"[POLLER] Status: {status}")

            if status == "redeemed":
                self._running = False
                # schedule callback on main thread since tkinter not thread safe
                self.root.after(0, self.on_redeemed)
                return

            if status == "expired":
                self._running = False
                return

            time.sleep(self.interval_s)