import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque
import os
from gpiozero import LED
from time import sleep
import threading
led = LED(17)
from ament_index_python.packages import get_package_share_directory

# ---------------- LOAD MODEL ----------------
pkg_path = get_package_share_directory('gesture_control')
model_path = os.path.join(pkg_path, 'gesture_model.pkl')

print("MODEL PATH:", model_path)

model = joblib.load(model_path)

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not detected")
    exit()

# ---------------- SMOOTHING ----------------
history = deque(maxlen=15)

gesture_to_command = {
    "Fist": "STAY",
    "open_palm": "STOP",
    "ok": "WALK",
    "peace": "BACKWARD",
    "thumbs_down": "SIT_DOWN",
    "thumbs_up": "STAND",
    "namaste": "NAMASTE",
    "one_finger": "FORWARD"
}

last_command = ""

# def led_pattern(command):
#     print("LED FUNCTION:", command)

#     # led.off()  # reset before new pattern

#     if command == "STAY":
#         led.on()

#     elif command == "STOP":
#         led.off()

#     elif command == "WALK":
#         for _ in range(3):
#             led.on()
#             sleep(1)
#             led.off()
#             sleep(1)

#     elif command == "BACKWARD":
#         for _ in range(6):
#             led.on()
#             sleep(0.2)
#             led.off()
#             sleep(0.2)

#     elif command == "SIT_DOWN":
#         for _ in range(2):
#             led.on()
#             sleep(0.5)
#             led.off()
#             sleep(0.5)

#     elif command == "STAND":
#         for _ in range(5):
#             led.on()
#             sleep(0.1)
#             led.off()
#             sleep(0.1)

#     elif command == "NAMASTE":
#         for _ in range(3):
#             led.on()
#             sleep(0.7)
#             led.off()
#             sleep(0.7)

#     elif command == "FORWARD":
#         led.on()
#         sleep(0.1)
#         led.off()
def led_worker(command):

    print("LED FUNCTION:", command)

    if command == "STAY":
        led.on()

    elif command == "STOP":
        led.off()

    elif command == "WALK":
        for _ in range(3):
            led.on()
            sleep(1)
            led.off()
            sleep(1)

    elif command == "BACKWARD":
        for _ in range(6):
            led.on()
            sleep(0.2)
            led.off()
            sleep(0.2)

    elif command == "SIT_DOWN":
        for _ in range(2):
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)

    elif command == "STAND":
        for _ in range(5):
            led.on()
            sleep(0.1)
            led.off()
            sleep(0.1)

    elif command == "NAMASTE":
        for _ in range(3):
            led.on()
            sleep(0.7)
            led.off()
            sleep(0.7)

    elif command == "FORWARD":
        led.on()
        sleep(0.1)
        led.off()


def led_pattern(command):

    thread = threading.Thread(
        target=led_worker,
        args=(command,),
        daemon=True
    )

    thread.start()

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    gesture = "No Hand"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            base_x = hand_landmarks.landmark[0].x
            base_y = hand_landmarks.landmark[0].y

            row = []
            for lm in hand_landmarks.landmark:
                row.append(lm.x - base_x)
                row.append(lm.y - base_y)
                row.append(lm.z)

            row = np.array(row).reshape(1, -1)

            # Prediction
            probs = model.predict_proba(row)
            confidence = np.max(probs)

            if confidence > 0.8:
                pred = model.predict(row)[0]
                history.append(pred)
                gesture = max(set(history), key=history.count)
            else:
                gesture = "Unknown"

            # ---------------- COMMAND ----------------
            if gesture in gesture_to_command:
                command = gesture_to_command[gesture]

                if command != last_command:
                    print("Robot Command:", command)
                    led_pattern(command)
                    last_command = command
                    # sleep(0.3)

    # ---------------- DISPLAY ----------------
    cv2.putText(frame, f"{gesture}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()



