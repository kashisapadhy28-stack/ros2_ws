import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ament_index_python.packages import get_package_share_directory

# ---------------- LOAD MODEL ----------------
pkg_path = get_package_share_directory('gesture_control')
model_path = os.path.join(pkg_path, 'gesture_model.pkl')

print("MODEL PATH:", model_path)

model = joblib.load(model_path)

# ---------------- ROS2 PUBLISHER ----------------
# rclpy.init()

# node = Node("gesture_publisher")

# publisher = node.create_publisher(
#     String,
#     "/gesture",
#     10
# )

class GesturePublisher(Node):

    def __init__(self):
        super().__init__('gesture_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/gesture',
            10
        )

        self.get_logger().info("Gesture Publisher Started")

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

rclpy.init()

node = GesturePublisher()

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

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
                    # print("Robot Command:", command)
                    msg = String()
                    msg.data = command

                    # publisher.publish(msg)
                    node.publisher_.publish(msg)

                    print("Published:", command)
                    last_command = command

    # ---------------- DISPLAY ----------------
    cv2.putText(frame, f"{gesture}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    rclpy.spin_once(node, timeout_sec=0)

    cv2.imshow("AI Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()