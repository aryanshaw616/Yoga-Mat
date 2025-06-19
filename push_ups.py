import cv2
import mediapipe as md
import math
import pyttsx3

engine1 = pyttsx3.init("sapi5")
engine1.setProperty("voice", engine1.getProperty("voices")[0].id)
engine1.setProperty("rate", 170)

def speak1(audio):
    engine1.say(audio)
    engine1.runAndWait()

def get_pushup_category(age, weight, gender):
    age, weight = int(age), int(weight)
    
    if gender == "female":
        return 20 if age <= 29 and weight < 70 else 18 if weight <= 90 else 15
    elif gender in ["male", "mail"]:
        return 24 if age <= 29 and weight < 60 else 20 if weight <= 75 else 15
    return 5  # Default minimum count

def start_pushups(age, height, weight, gender):
    pushup_goal = get_pushup_category(age, weight, gender)
    speak1(f"Aim for at least {pushup_goal} push-ups. Let's begin!")

    md_drawing = md.solutions.drawing_utils
    md_pose = md.solutions.pose

    count = 0
    position = None
    cap = cv2.VideoCapture(0)

    def calculate_angle(a, b, c):
        radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        angle = abs(math.degrees(radians))
        return 360 - angle if angle > 180.0 else angle

    with md_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Empty camera feed")
                break

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            result = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            imlist = []

            if result.pose_landmarks:
                md_drawing.draw_landmarks(image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)
                for id, im in enumerate(result.pose_landmarks.landmark):
                    h, w, _ = image.shape
                    X, Y = int(im.x * w), int(im.y * h)
                    imlist.append([id, X, Y])

            if len(imlist) != 0:
                left_elbow_angle = calculate_angle(imlist[11][1:], imlist[13][1:], imlist[15][1:])
                right_elbow_angle = calculate_angle(imlist[12][1:], imlist[14][1:], imlist[16][1:])

                elbows_bent = (left_elbow_angle <= 55 or right_elbow_angle <= 55)
                hips_low = (imlist[12][2] and imlist[11][2] >= imlist[14][2] and imlist[13][2])

                if hips_low and elbows_bent:
                    if position != "down":
                        position = "down"
                elif hips_low and not elbows_bent:
                    cv2.putText(image, "Bend elbows more!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif not hips_low and elbows_bent:
                    cv2.putText(image, "Lower your chest more!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    position = None

                if (imlist[12][2] and imlist[11][2] <= imlist[14][2] and imlist[13][2] and position == "down"):
                    position = "up"
                    count += 1
                    print(count)

            cv2.imshow("Push-up Counter", cv2.flip(image, 1))
            key = cv2.waitKey(1)
            if key == ord('q') or count >= pushup_goal:
                break

    cap.release()
    speak1("Great job! You have completed your push-ups.")
