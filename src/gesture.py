"""
Gesture, color and mode management.
"""

from config import COLORS


class GestureController:
    def __init__(self):
        self.colors = COLORS
        self.color_index = 0
        self.mode = "idle"  # idle | draw | erase

    @property
    def current_color(self):
        return self.colors[self.color_index]

    def set_color(self, index):
        if 0 <= index < len(self.colors):
            self.color_index = index
            print(f"[INFO] Color changed → {index + 1}")

    def set_mode(self, mode: str):
        self.mode = mode

    def get_status_text(self):
        if self.mode == "draw":
            return "DRAWING"
        elif self.mode == "erase":
            return "ERASER"
        return "READY"