import cv2
import tkinter as tk
from PIL import Image, ImageTk

# webcam url, must be on same wi-fi
# using "IP Webcam" on playstore
STREAM_URL = "http://192.168.1.196:8080/video"

class CameraFeed:
    def __init__(self, root):
        self.root = root
        self.root.title("Recycle Rewards — Scanner")

        self.label = tk.Label(root)
        self.label.pack()

        self.cap = cv2.VideoCapture(STREAM_URL)
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.root.after(30, self.update)

    def release(self):
        self.cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraFeed(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.release(), root.destroy()))
    root.mainloop()