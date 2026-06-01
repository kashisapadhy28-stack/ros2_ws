from setuptools import find_packages, setup

package_name = 'gesture_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/gesture_control', ['gesture_control/gesture_model.pkl']),
        ('share/gesture_control/launch', ['launch/gesture_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='seeya',
    maintainer_email='seeya@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'detect_gesture = gesture_control.detect_gesture:main',
            'led_node = gesture_control.led_node:main',
            'led_controller = gesture_control.led_controller:main',
            'motor_control = gesture_control.motor_control:main',
            
        ],
    },
)
