from assistant_utils import speak1
import time

def squats():
    speak1("Let's do squats. Perform 10 repetitions.")
    for i in range(1, 11):
        speak1(f"Squat {i}")
        time.sleep(2)
    speak1("Well done! You finished the set.")

if __name__ == "__main__":
    squats()
