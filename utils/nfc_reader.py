import queue
import threading
from flask import Flask, request, render_template_string

# READ ME!!!!!!!!!!!!!!!!!!!!!!

# 1. download:
# samsung drivers https://developer.samsung.com/android-usb-driver
# android sdk https://developer.android.com/tools/releases/platform-tools
# add extracted adb folder (with all the executables) to Windows environment path variables

# 2. connect android phone
# 3. on popup change permissions to transfer files
# 4. activate developer mode on phone
# 5. developer option -> USB Debugging (turn on)
# 6. run these commands to verify adb is installed and phone recognised:
'''
adb kill-server
adb start-server
adb devices
'''
# 7. run command "adb reverse tcp:5000 tcp:5000"
# 8. run debug
# 9. on phone run "localhost:5000" in Chrome
# 10. scan with NDEF format NFC (not low freq RFID and not debit cards (EMV format))

nfc_queue: queue.Queue = queue.Queue()

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
    uid = request.json.get('uid')
    print(f"[NFC] UID received: {uid}")
    nfc_queue.put(uid)
    return {'status': 'ok'}

def start():
    threading.Thread(target=lambda: _app.run(port=5000), daemon=True).start()