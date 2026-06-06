import tkinter as tk
from ui.style import *

class ScanningScreen(tk.Frame):
    def __init__(self, parent: tk.Misc, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="INSERT BOTTLES OR CANS", font=FONT_HEADING, bg=BG, fg=TEXT).pack(pady=(60, 0))

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True)

        # bottles and cans side by side
        counters = tk.Frame(center, bg=BG)
        counters.pack()

        bottle_frame = tk.Frame(counters, bg=BG)
        bottle_frame.pack(side=tk.LEFT, padx=60)

        tk.Label(bottle_frame, text="bottles", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        self._bottle_label = tk.Label(bottle_frame, text="0", font=FONT_COUNTER, bg=BG, fg=ACCENT)
        self._bottle_label.pack()

        can_frame = tk.Frame(counters, bg=BG)
        can_frame.pack(side=tk.LEFT, padx=60)

        tk.Label(can_frame, text="cans", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        self._can_label = tk.Label(can_frame, text="0", font=FONT_COUNTER, bg=BG, fg=ACCENT)
        self._can_label.pack()

        tk.Frame(center, height=40, bg=BG).pack()

        tk.Label(center, text="points earned", font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack()
        self._points_label = tk.Label(center, text="0", font=FONT_COUNTER, bg=BG, fg=ACCENT)
        self._points_label.pack()

    def update_counts(self, bottles: int, cans: int):
        self._bottle_label.configure(text=str(bottles))
        self._can_label.configure(text=str(cans))

    def update_points(self, points: int):
        self._points_label.configure(text=str(points))

    def on_show(self):
        pass