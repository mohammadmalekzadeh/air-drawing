"""
Configuration settings for Air Drawing application.
"""

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Drawing settings
BRUSH_THICKNESS = 8
ERASER_THICKNESS = 40

COLORS = [
    (0, 0, 255),      # Red
    (0, 255, 0),      # Green
    (255, 0, 0),      # Blue
    (0, 255, 255),    # Yellow
    (255, 0, 255),    # Magenta
    (255, 255, 0),    # Cyan
    (255, 255, 255),  # White
]

# MediaPipe settings
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

# UI Layout
COLOR_BOX_SIZE = 60
COLOR_BOX_MARGIN = 15
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 55
BUTTON_MARGIN = 20

# Cooldown (to prevent multiple triggers)
ACTION_COOLDOWN = 1.0  # seconds