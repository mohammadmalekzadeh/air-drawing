"""
Entry point of the Air Drawing application.
"""

from src.app import AirDrawingApp


def main():
    try:
        app = AirDrawingApp()
        app.run()
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()