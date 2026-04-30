FROM ros:humble

RUN apt update && apt install -y \
    python3-pip \
    python3-opencv \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    mediapipe==0.10.9 \
    opencv-contrib-python \
    numpy \
    joblib \
    scikit-learn

# ✅ ONLY copy src folder
COPY src /ros2_ws/src

WORKDIR /ros2_ws

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

CMD ["bash"]
