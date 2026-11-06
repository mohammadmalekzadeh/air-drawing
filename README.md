# Air Drawing

Professional real-time hand gesture drawing application built with Python, OpenCV, and MediaPipe.

Draw in the air using only your webcam and hand gestures. Fully controlled through an on-screen interface — no keyboard required for main actions.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- Real-time hand tracking with MediaPipe
- Draw with Index finger
- Eraser with Thumb
- On-screen color palette (touch to select)
- On-screen buttons: Clear / Save / Exit
- Fully gesture-controlled interface
- Clean modular architecture

---

## Project Structure

```
air-drawing/
├── main.py                 # Entry point
├── config.py               # All settings and constants
├── requirements.txt
├── .gitignore
├── README.md
└── src/
    ├── __init__.py
    ├── app.py              # Main application logic + UI
    ├── hand_tracker.py     # MediaPipe hand detection
    ├── canvas.py           # Drawing & erasing canvas
    └── gesture.py          # Mode and color management
```

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/air-drawing.git
cd air-drawing

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

---

## Controls

| Action              | Gesture / Interaction                     |
|---------------------|-------------------------------------------|
| Draw                | Raise only Index finger                   |
| Eraser              | Raise only Thumb                          |
| Change Color        | Point Index finger to a color box         |
| Clear Canvas        | Point to **CLEAR** button                 |
| Save Drawing        | Point to **SAVE** button                  |
| Exit Program        | Point to **EXIT** button                  |

---

## Requirements

- Python 3.9 or higher
- Webcam
- Windows / macOS / Linux

---

## Dependencies

- `opencv-python`
- `mediapipe`
- `numpy`

---

## License

This project is licensed under the MIT License.