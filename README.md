\# ROS2 Gesture Control System



\## Project Overview

Hand gesture controlled robotic system using:



\- MediaPipe

\- OpenCV

\- Machine Learning

\- ROS2 Jazzy

\- Raspberry Pi 5

\- GPIO LED Feedback



\## Features



\- Gesture Recognition

\- ROS2 Publisher

\- ROS2 Subscriber

\- LED Pattern Control

\- Launch File Support



\## Gesture Mapping



| Gesture | Command |

|----------|----------|

| Fist | STAY |

| Open Palm | STOP |

| OK | WALK |

| Peace | BACKWARD |

| Thumbs Down | SIT\_DOWN |

| Thumbs Up | STAND |

| Namaste | NAMASTE |

| One Finger | FORWARD |



\## Run



```bash

source /opt/ros/jazzy/setup.bash

source install/setup.bash

ros2 launch gesture\_control gesture\_system.launch.py

