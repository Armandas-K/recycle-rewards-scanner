import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraFeed:
    def __init__(self, root: tk.Misc, source, on_frame=None, display: bool = True, display_scale: float = 1.0):
        self.root = root
        self.on_frame = on_frame
        self.display = display
        self.display_scale = display_scale
        self.label = None

        if display:
            self.label = tk.Label(root)
            self.label.pack()

        # webcam or url
        self.cap = cv2.VideoCapture(source)
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            # pass frame to scanner before displaying
            if self.on_frame:
                self.on_frame(frame)

            if self.display and self.label:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.display_scale != 1.0:
                    h, w = frame_rgb.shape[:2]
                    frame_rgb = cv2.resize(
                        frame_rgb,
                        (int(w * self.display_scale), int(h * self.display_scale))
                    )

                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)

        self.root.after(30, self.update)

    def release(self):
        self.cap.release()