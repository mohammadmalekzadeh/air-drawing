"""
Canvas management for drawing and erasing.
"""

import cv2
import numpy as np
import time
from config import BRUSH_THICKNESS, ERASER_THICKNESS


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_point = None
        self.brush_thickness = BRUSH_THICKNESS
        self.eraser_thickness = ERASER_THICKNESS

    def draw_line(self, point, color, is_eraser=False):
        if self.prev_point is None:
            self.prev_point = point
            return

        thickness = self.eraser_thickness if is_eraser else self.brush_thickness
        cv2.line(self.canvas, self.prev_point, point, color, thickness)
        self.prev_point = point

    def reset_previous_point(self):
        self.prev_point = None

    def clear(self):
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.prev_point = None
        print("[INFO] Canvas cleared.")

    def save(self, prefix="drawing"):
        filename = f"{prefix}_{int(time.time())}.png"
        cv2.imwrite(filename, self.canvas)
        print(f"[INFO] Drawing saved as: {filename}")
        return filename

    def get_canvas(self):
        return self.canvas

    def overlay_on_frame(self, frame):
        mask = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        return cv2.add(frame_bg, canvas_fg)