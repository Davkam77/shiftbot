import threading
import time
from bot.grabber_task import grab_all_shifts

def start_background_grabber(interval=600):
    def loop():
        while True:
            print("[GRABBER] Запуск фонового бронирования...")
            grab_all_shifts()
            time.sleep(interval)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


if __name__ == "__main__":
    print(">>> Ручной запуск задачи бронирования смен...")
    grab_all_shifts()
