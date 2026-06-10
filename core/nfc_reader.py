import queue
import threading
import time
from flask import Flask, request, render_template_string

NFC_COOLDOWN = 3  # seconds - ignore same uid

nfc_queue: queue.Queue = queue.Queue()
_last_uid: str = ""
_last_time: float = 0.0

_app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<body>
    <h2>NFC Reader</h2>
    <button id="btn" style="padding:20px;font-size:20px">Start Scanning</button>
    <p id="status">Press button to begin</p>
    <script>
        document.getElementById('btn').addEventListener('click', async () => {
            try {
                const reader = new NDEFReader();
                await reader.scan();
                document.getElementById('status').textContent = 'Waiting for tap...';

                reader.onreading = e => {
                    const uid = e.serialNumber;
                    document.getElementById('status').textContent = 'Read: ' + uid;
                    fetch('/nfc', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ uid: uid })
                    });
                };

                reader.onerror = e => {
                    document.getElementById('status').textContent = 'NFC error: ' + e.message;
                };

            } catch (err) {
                document.getElementById('status').textContent = 'Failed: ' + err.message;
            }
        });
    </script>
</body>
</html>
"""

@_app.route('/')
def index():
    return render_template_string(HTML)

@_app.route('/nfc', methods=['POST'])
def receive_nfc():
    global _last_uid, _last_time

    uid = request.json.get('uid')
    now = time.time()

    if uid == _last_uid and now - _last_time < NFC_COOLDOWN:
        print(f"[NFC] Duplicate read ignored: {uid}")
        return {'status': 'ok'}

    _last_uid = uid
    _last_time = now

    print(f"[NFC] UID received: {uid}")
    nfc_queue.put(uid)
    return {'status': 'ok'}

def start():
    threading.Thread(target=lambda: _app.run(port=5000), daemon=True).start()