# AI Gesture Recognition with ROS2

## Overview

An AI-powered hand gesture recognition system built using MediaPipe, OpenCV, Machine Learning, and ROS2 Jazzy.

The system detects hand gestures in real time, classifies them using a trained machine learning model, and publishes commands through ROS2 for robotic control. GPIO LEDs provide visual feedback for recognized gestures.

## Hardware

- Raspberry Pi 5
- USB Camera
- GPIO LEDs

## Software Stack

- Python
- ROS2 Jazzy
- OpenCV
- MediaPipe
- Scikit-learn

## Features

- Real-time hand tracking
- Machine learning based gesture classification
- ROS2 Publisher/Subscriber communication
- Launch file support
- LED feedback system
- Modular ROS2 package structure

## Gesture Mapping

| Gesture | Command |
|----------|----------|
| Fist | STAY |
| Open Palm | STOP |
| OK | WALK |
| Peace | BACKWARD |
| Thumbs Down | SIT_DOWN |
| Thumbs Up | STAND |
| Namaste | NAMASTE |
| One Finger | FORWARD |

## Project Structure

src/
└── gesture_control/
    ├── detect_gesture.py
    ├── gesture_model.pkl
    ├── led_controller.py
    ├── launch/
    └── resource/

## Running the Project

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch gesture_control gesture_system.launch.py
