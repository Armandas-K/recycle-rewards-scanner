import tkinter as tk
from ui.style import *

class ScanningScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="INSERT BOTTLES", font=FONT_HEADING, bg=BG, fg=TEXT).pack(pady=(60, 0))

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True)

        tk.Label(center, text="bottles scanned", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        self._bottle_label = tk.Label(center, text="0", font=FONT_COUNTER, bg=BG, fg=ACCENT)
        self._bottle_label.pack()

        tk.Frame(center, height=40, bg=BG).pack()

        tk.Label(center, text="points earned", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        self._points_label = tk.Label(center, text="0", font=FONT_COUNTER, bg=BG, fg=ACCENT)
        self._points_label.pack()

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(fill=tk.X, padx=40, pady=40)

        tk.Button(
            bottom,
            text="CHECKOUT",
            font=FONT_BUTTON,
            bg=ACCENT,
            fg=BTN_TEXT,
            padx=20, pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.app.go_loading
        ).pack(side=tk.RIGHT)

    def update_count(self, count: int):
        self._bottle_label.configure(text=str(count))

    def update_points(self, points: int):
        self._points_label.configure(text=str(points))

    def on_show(self):
        pass