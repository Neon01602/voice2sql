from .voice_sql import run_main
import threading
import time

def main():
    threading.Thread(target=run_main, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Program terminated.")
