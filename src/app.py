"""
Main application logic with on-screen UI.
"""

import cv2
import time
from config import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    COLORS, COLOR_BOX_SIZE, COLOR_BOX_MARGIN,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN,
    ACTION_COOLDOWN
)
from src.hand_tracker import HandTracker
from src.canvas import Canvas
from src.gesture import GestureController


class AirDrawingApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Cannot access webcam.")

        self.h, self.w = frame.shape[:2]
        self.tracker = HandTracker()
        self.canvas = Canvas(self.w, self.h)
        self.gesture = GestureController()

        self.last_action_time = 0

        # UI Regions
        self.color_boxes = self._create_color_boxes()
        self.buttons = self._create_buttons()

    def _create_color_boxes(self):
        boxes = []
        start_x = COLOR_BOX_MARGIN
        y = COLOR_BOX_MARGIN

        for i, color in enumerate(COLORS):
            x1 = start_x + i * (COLOR_BOX_SIZE + COLOR_BOX_MARGIN)
            y1 = y
            x2 = x1 + COLOR_BOX_SIZE
            y2 = y1 + COLOR_BOX_SIZE
            boxes.append({
                "id": i,
                "rect": (x1, y1, x2, y2),
                "color": color
            })
        return boxes

    def _create_buttons(self):
        buttons = []
        labels = ["CLEAR", "SAVE", "EXIT"]
        start_y = self.h - (BUTTON_HEIGHT + BUTTON_MARGIN) * 3 - 20

        for i, label in enumerate(labels):
            x1 = self.w - BUTTON_WIDTH - BUTTON_MARGIN
            y1 = start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            x2 = x1 + BUTTON_WIDTH
            y2 = y1 + BUTTON_HEIGHT
            buttons.append({
                "id": label,
                "rect": (x1, y1, x2, y2),
                "label": label
            })
        return buttons

    def _point_in_rect(self, x, y, rect):
        x1, y1, x2, y2 = rect
        return x1 <= x <= x2 and y1 <= y <= y2

    def _can_trigger(self):
        return (time.time() - self.last_action_time) > ACTION_COOLDOWN

    def _draw_ui(self, frame):
        # Color palette
        for box in self.color_boxes:
            x1, y1, x2, y2 = box["rect"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), box["color"], -1)
            if box["id"] == self.gesture.color_index:
                cv2.rectangle(frame, (x1-3, y1-3), (x2+3, y2+3), (255, 255, 255), 3)

        # Buttons
        for btn in self.buttons:
            x1, y1, x2, y2 = btn["rect"]
            color = (40, 40, 40)
            if btn["id"] == "EXIT":
                color = (0, 0, 180)
            elif btn["id"] == "CLEAR":
                color = (0, 100, 0)
            elif btn["id"] == "SAVE":
                color = (180, 100, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

            text_size = cv2.getTextSize(btn["label"], cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_x = x1 + (BUTTON_WIDTH - text_size[0]) // 2
            text_y = y1 + (BUTTON_HEIGHT + text_size[1]) // 2
            cv2.putText(frame, btn["label"], (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Status
        status = self.gesture.get_status_text()
        color = (0, 255, 0) if status == "DRAWING" else (0, 165, 255) if status == "ERASER" else (200, 200, 200)
        cv2.putText(frame, status, (20, self.h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    def run(self):
        print("=" * 60)
        print("  Air Drawing - Full On-Screen Gesture Control")
        print("=" * 60)
        print("How to use:")
        print("  • Only Index finger up     → Draw")
        print("  • Only Thumb up            → Eraser")
        print("  • Point to a color box     → Change color")
        print("  • Point to CLEAR / SAVE / EXIT buttons")
        print("=" * 60)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            detection_result = self.tracker.process(frame)

            finger_x, finger_y = None, None

            if detection_result.hand_landmarks:
                self.tracker.draw_landmarks(frame, detection_result)

                for hand_landmarks in detection_result.hand_landmarks:
                    index_x, index_y = self.tracker.get_index_finger_tip(
                        hand_landmarks, self.w, self.h
                    )
                    finger_x, finger_y = index_x, index_y

                    # Mode detection
                    if self.tracker.is_index_up(hand_landmarks):
                        self.gesture.set_mode("draw")
                        cv2.circle(frame, (index_x, index_y), 12, self.gesture.current_color, -1)
                        self.canvas.draw_line((index_x, index_y), self.gesture.current_color, is_eraser=False)

                    elif self.tracker.is_thumb_up(hand_landmarks):
                        self.gesture.set_mode("erase")
                        thumb_x, thumb_y = self.tracker.get_thumb_tip(hand_landmarks, self.w, self.h)
                        cv2.circle(frame, (thumb_x, thumb_y), 18, (50, 50, 50), -1)
                        self.canvas.draw_line((thumb_x, thumb_y), (0, 0, 0), is_eraser=True)

                    else:
                        self.gesture.set_mode("idle")
                        self.canvas.reset_previous_point()

            # Check UI interactions
            if finger_x is not None and self._can_trigger():
                # Color selection
                for box in self.color_boxes:
                    if self._point_in_rect(finger_x, finger_y, box["rect"]):
                        self.gesture.set_color(box["id"])
                        self.last_action_time = time.time()
                        break

                # Buttons
                for btn in self.buttons:
                    if self._point_in_rect(finger_x, finger_y, btn["rect"]):
                        if btn["id"] == "CLEAR":
                            self.canvas.clear()
                        elif btn["id"] == "SAVE":
                            self.canvas.save()
                        elif btn["id"] == "EXIT":
                            self.cleanup()
                            return
                        self.last_action_time = time.time()
                        break

            # Draw UI
            self._draw_ui(frame)

            # Overlay canvas
            combined = self.canvas.overlay_on_frame(frame)

            cv2.imshow("Air Drawing", combined)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.tracker.close()
        print("[INFO] Application closed.")