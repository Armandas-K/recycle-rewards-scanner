# Recycle Rewards Scanner

A barcode scanning application that rewards users with points for recycling plastic bottles and aluminium cans. Developed as part of the Engineers Without Borders [Engineering for People Design Challenge](https://www.ewb-uk.org) for Ladywood, Birmingham.

> This app requires the web app to function fully
> [Web app](https://github.com/vvolcauskas/CMP-LP-PRO-2026) (private repo - only for contributors)

---

## Requirements

- Python 3.13
- Webcam or [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam) (Android)
- Android phone with NFC
- USB-C data cable
- [Samsung USB Drivers](https://developer.samsung.com/android-usb-driver) (for samsung devices)
- [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) - extract and add the folder to Windows environment PATH

---

## Installing Dependencies

### PyCharm (recommended)

1. Open the project in PyCharm
2. Go to **Python Packages** tab on the bottom left
3. Using the PyPI search bar install the packages below:

| Package       | Version   |
|---------------|-----------|
| opencv-python | 4.13.0.92 |
| pandas        | 3.0.3     |
| Pillow        | 12.2.0    |
| pyzbar        | 0.1.9     |
| requests      | 2.34.2    |
| numpy         | 2.4.6     |
| pytest        | 9.0.3     |
| flask         | 3.1.3     |

### pip

```bash
pip install opencv-python pandas Pillow pyzbar requests numpy pytest flask
```

---

## NFC Setup

NFC is handled through an Android phone connected to the pc via USB, running a web NFC page in Chrome that forwards to the python code

> Only works on Android with Chrome, not IOS

### Steps

1. Connect the Android phone to the PC via USB
2. On the phone notification popup, set USB mode to **Transfer files**
3. Enable **Developer Mode** on the phone
4. In **Developer Options**, enable **USB Debugging**
5. Run the following to verify ADB can see the phone:

```bash
adb kill-server
adb start-server
adb devices
```

The device should appear as `device` not `unauthorized`. If `unauthorized`, look for an **Allow USB Debugging** popup and tap **Allow**

6. Run the port reverse command:

```bash
adb reverse tcp:5000 tcp:5000
```

7. Run `debug.py` or `main.py`
8. Open `localhost:5000` in Chrome on the phone
9. Tap **Start Scanning**, then tap an NFC tag or phone to the back of the Android

> Tags must be NDEF format

---

## Setup

### Build the barcode cache

```bash
python build_cache.py
```

---

## Running

### Debug

```bash
python debug.py
```

Runs the full UI with the camera feed displayed in a separate window and debug console logging

**Camera source** - edit the top of `debug.py`:

```python
STREAM_URL = "http://192.168.1.196:8080/video"

# set to 0 for webcam, change index if wrong camera is selected
CAMERA_SOURCE = STREAM_URL
# CAMERA_SOURCE = 0
```

To use an Android phone as the camera:
1. Install **IP Webcam** from the Play Store
2. Open the app and tap **Start server** at the bottom
3. Replace the IP in `STREAM_URL` with the address on screen and add `/video` to the end
4. Both devices must be on the same wifi network

### Main

```bash
python main.py
```

Production entry point, differences from debug:

- Fullscreen UI (esc to exit)
- No camera feed window
- No console UID input - NFC tap required
- Only accepts barcodes found in the local cache - no Open Food Facts API fallback
- Requires the user's NFC UID to be registered in the backend
- Less verbose console logging

### Tests

```bash
pytest tests/
```

---

## Troubleshooting

### pyzbar ImportError on Windows

If you get an `ImportError` for a missing `libzbar-64.dll`, install the Visual Studio C++ Redistributable:

[Download vcredist_x64.exe](https://www.microsoft.com/en-US/download/details.aspx?id=40784)