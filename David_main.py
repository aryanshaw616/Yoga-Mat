import datetime
from email import message
import time
import webbrowser
from numpy import tile
import psutil
import pyttsx3
import speech_recognition
import requests
from bs4 import BeautifulSoup
import os
import pyautogui
import random
from plyer import notification
from pygame import mixer
import speedtest
import threading

engine1 = pyttsx3.init("sapi5")
voices1 = engine1.getProperty("voices")
engine1.setProperty("voice", voices1[0].id)
rate1 = engine1.setProperty("rate",170)

def speak1(audio):
    engine1.say(audio)
    engine1.runAndWait()

def fetch_joke():
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    response = requests.get(url)
    joke_data = response.json()
    
    if joke_data['type'] == 'single':
        joke = joke_data['joke']
    else:
        joke = f"{joke_data['setup']} - {joke_data['delivery']}"
    
    return joke

def takeCommand1():
    r1 = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....Speak now ")
        r1.pause_threshold = 1
        r1.energy_threshold = 300
        audio = r1.listen(source,0,4)

    try:
        print("Understanding..")
        query1  = r1.recognize_google(audio,language='en-in')
        print(f"You Said: {query1}\n")
    except Exception as e:
        speak1("Say that again please ")
        print("Say that again please ")
        return "None"
    return query1


for i in range(10):
    speak1("Enter the password to open the Yoga Mat Assistant")
    a = input("Enter Password: ").strip().lower()  
    pw_file = open("password.txt", "r")
    pw = pw_file.read().strip().lower()  
    pw_file.close()
    
    if a == pw:
        speak1("WELCOME SIR! PLEASE SPEAK [WAKE UP] TO LOAD ME UP")
        print("WELCOME SIR! PLEASE SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif i == 2:
        exit()
    else:
        print("Wrong password! Retry")

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception:
        print("Say that again")
        return "None"
    return query
def start_exercise():
    global age, height, weight  

    def get_voice_input(prompt):
        for _ in range(4):  
            speak1(prompt)
            response = takeCommand1().strip()
            if response and response.lower() != "none":
                return response
            speak1("I didn't catch that. Please say it again.")
        speak1("Too many failed attempts. Please try again later.")
        return None  

    age = get_voice_input("Please say your age.")
    if not age:
        return
    
    height = get_voice_input("Now, say your height in centimeters.")
    if not height:
        return
    
    weight = get_voice_input("Finally, say your weight in kilograms.")
    if not weight:
        return

    speak1("Your details have been recorded. Now, say the exercise you want to start.")


def alarm(query):
    timehere = open("Alarmtext.txt", "a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def hydration_reminder():
    mixer.init()
    while True:
        time.sleep(30) 
        mixer.music.load("notification.mp3")
        mixer.music.play()
        time.sleep(3)  # Wait for the sound to play fully
        
        notification.notify(
            title="Hydration Reminder",
            message="Drink some water to stay hydrated!",
            timeout=10
        )
        speak("Reminder: Please drink water to stay hydrated.")

# Start hydration reminder in a separate thread
threading.Thread(target=hydration_reminder, daemon=True).start()

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can call me anytime")
                    break 
                
                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = takeCommand1().lower()
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done sir")
                    speak(f"Your new password is{new_pw}")

                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()

                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                    )
                    speak(message)

                elif "focus mode" in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        speak("Entering the focus mode....")
                        os.startfile("D:\\Coding\\Youtube\\David VA\\FocusMode.py")
                        exit()

                    else:
                        pass

                elif "show my focus" in query:
                    from FocusGraph import focus_graph
                    focus_graph()

                elif "translate" in query:
                    from Translator import translategl
                    query = query.replace("David","")
                    query = query.replace("translate","")
                    translategl(query)

                elif "open" in query:   
                    query = query.replace("open","")
                    query = query.replace("David","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")                       
                     
                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                     import pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")

                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                elif "i am fine" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                
                elif "tired" in query:
                    speak("Playing your favourite songs, sir")
                    webbrowser.open("https://youtu.be/2g5xkLqIElU")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
                elif "start exercise" in query:
                    start_exercise()

                elif "push ups" in query:
                    os.system("python push_ups.py")
                elif "squats" in query:
                    os.system("python squats.py")
                elif "jumping jacks" in query:
                    os.system("python jumping_jacks.py")
                elif "lunges" in query:
                    os.system("python lunges.py")
                elif "plank" in query:
                    os.system("python plank.py")
                elif "high knees" in query:
                    os.system("python high_knees.py")
                elif "side leg raises" in query:
                    os.system("python side_leg_raises.py")
                elif "warrior pose" in query or "yoga warrior" in query:
                    os.system("python yoga_warrior_pose.py")
                elif "sit ups" in query:
                    os.system("python sit_ups.py")
                elif "burpees" in query:
                    os.system("python burpees.py")

                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)

                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()

                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()

                elif ("temperature" or "tell me about weather" or "weather") in query:
                    search = "temperature in Kolkata"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")
                           
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()
                
                
                elif 'check battery status' in query:
                        battery = psutil.sensors_battery()
                        percentage = battery.percent
                        speak(f"Your system's battery is at {percentage}%.")
                
                elif 'play a joke' in query:
                    speak("Let me tell you a joke.")
                    joke = fetch_joke()
                    speak(joke)
        
                
                    
                elif 'what is the uptime' in query:
                    uptime_seconds = time.time() - psutil.boot_time()
                    uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
                    speak(f"Your system has been up for {uptime_string}.")
    
                elif 'how much is my cpu usage' in query:
                        cpu_usage = psutil.cpu_percent(interval=1)
                        speak(f"Your CPU usage is currently at {cpu_usage} percent.")
                    
                elif 'check my ram usage' in query:
                        memory = psutil.virtual_memory()
                        ram_usage = memory.percent
                        speak(f"Your RAM usage is currently at {ram_usage} percent.")
               
                elif'shut up' in query:
                    speak("are u in a bad mood sir ?")
                    speak("I appreciate your peace , talk ko me when you require till then I am going to have a nice sleep   bye")
        

                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("David","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())

                elif "shutdown system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break