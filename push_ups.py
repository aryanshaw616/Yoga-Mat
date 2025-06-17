
from assistant_utils import speak1
import time

def push_ups():
    speak1("Let's begin push-ups. Do 10 repetitions.")
    for i in range(1, 11):
        speak1(f"Push-up {i}")
        time.sleep(2)
    speak1("Great job! You completed the set.")

if __name__ == "__main__":
    push_ups()
