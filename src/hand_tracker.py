"""
Hand tracking module using the new MediaPipe Tasks API.
"""

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import urllib.request
import os


class HandTracker:
    def __init__(self):
        # Download the model if it doesn't exist
        model_path = "hand_landmarker.task"
        if not os.path.exists(model_path):
            print("[INFO] Downloading hand landmarker model...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, model_path)
            print("[INFO] Model downloaded.")

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process(self, frame):
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        return self.detector.detect(mp_image)

    def draw_landmarks(self, frame, detection_result):
        if not detection_result.hand_landmarks:
            return

        for hand_landmarks in detection_result.hand_landmarks:
            for landmark in hand_landmarks:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

            # Draw connections (simplified)
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),          # Thumb
                (0, 5), (5, 6), (6, 7), (7, 8),          # Index
                (0, 9), (9, 10), (10, 11), (11, 12),     # Middle
                (0, 13), (13, 14), (14, 15), (15, 16),   # Ring
                (0, 17), (17, 18), (18, 19), (19, 20),   # Pinky
                (5, 9), (9, 13), (13, 17)                # Palm
            ]
            h, w = frame.shape[:2]
            for start, end in connections:
                x1 = int(hand_landmarks[start].x * w)
                y1 = int(hand_landmarks[start].y * h)
                x2 = int(hand_landmarks[end].x * w)
                y2 = int(hand_landmarks[end].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    def get_index_finger_tip(self, hand_landmarks, frame_width, frame_height):
        landmark = hand_landmarks[8]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        return x, y

    def get_thumb_tip(self, hand_landmarks, frame_width, frame_height):
        landmark = hand_landmarks[4]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        return x, y

    def is_index_up(self, hand_landmarks):
        """Only index finger is raised → Drawing mode"""
        index_up = hand_landmarks[8].y < hand_landmarks[6].y
        middle_up = hand_landmarks[12].y < hand_landmarks[10].y
        ring_up = hand_landmarks[16].y < hand_landmarks[14].y
        pinky_up = hand_landmarks[20].y < hand_landmarks[18].y
        return index_up and not middle_up and not ring_up and not pinky_up

    def is_thumb_up(self, hand_landmarks):
        """Only thumb is raised → Eraser mode"""
        thumb_up = hand_landmarks[4].y < hand_landmarks[3].y
        index_up = hand_landmarks[8].y < hand_landmarks[6].y
        middle_up = hand_landmarks[12].y < hand_landmarks[10].y
        ring_up = hand_landmarks[16].y < hand_landmarks[14].y
        pinky_up = hand_landmarks[20].y < hand_landmarks[18].y
        return thumb_up and not index_up and not middle_up and not ring_up and not pinky_up

    def close(self):
        self.detector.close()