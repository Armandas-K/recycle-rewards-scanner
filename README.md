# Recycle Rewards Scanner

A barcode scanning application that rewards users with points for recycling plastic bottles and aluminium cans. Developed as part of the Engineers Without Borders [Engineering for People Design Challenge](https://www.ewb-uk.org) for Ladywood, Birmingham.

> This app requires the web app to function fully. (when API is implemented fully)\
> [Web app](https://github.com/vvolcauskas/CMP-LP-PRO-2026) (private repo - only for contributors)

---

## Requirements

- Python 3.13
- Webcam or [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam) (Android)

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
| qrcode        | 8.2       |
| requests      | 2.34.2    |
| numpy         | 2.4.6     |

### pip

```bash
pip install opencv-python pandas Pillow pyzbar qrcode requests numpy
```

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

**Camera source** — edit the top of `debug.py`:

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

### Main *(does not work yet)*

```bash
python main.py
```

Production entry point using the built-in webcam. Backend API communication not yet implemented.