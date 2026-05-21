from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='gesture_control',
            executable='detect_gesture',
            name='gesture_detector',
            output='screen'
        ),

        Node(
            package='gesture_control',
            executable='led_controller',
            name='led_controller',
            output='screen'
        )

    ])
