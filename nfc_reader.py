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
# 8. run this python script
# 9. on phone run "localhost:5000" in Chrome
# 10. scan with NDEF format NFC (not low freq RFID and not debit cards (EMV format))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<body>
    <h2>NFC Reader Active</h2>
    <p id="status">Waiting for tap...</p>
    <script>
        const status = document.getElementById('status');
        async function startNFC() {
            const reader = new NDEFReader();
            await reader.scan();
            reader.onreading = e => {
                const uid = e.serialNumber;
                status.textContent = 'Read: ' + uid;
                fetch('/nfc', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ uid: uid })
                });
            };
        }
        startNFC();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/nfc', methods=['POST'])
def receive_nfc():
    uid = request.json.get('uid')
    print(f"[NFC] UID received: {uid}")
    # TODO: forward uid to backend
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)