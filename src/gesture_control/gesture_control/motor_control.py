import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from gpiozero import OutputDevice


# Left motor
in1 = OutputDevice(17)
in2 = OutputDevice(27)

# Right motor
in3 = OutputDevice(22)
in4 = OutputDevice(23)


def forward():
    print("FORWARD")

    in1.on()
    in2.off()

    in3.on()
    in4.off()


def backward():
    print("BACKWARD")

    in1.off()
    in2.on()

    in3.off()
    in4.on()


def stop():
    print("STOP")

    in1.off()
    in2.off()

    in3.off()
    in4.off()


class MotorControlNode(Node):

    def __init__(self):
        super().__init__('motor_control_node')

        self.subscription = self.create_subscription(
            String,
            '/gesture',
            self.gesture_callback,
            10
        )

        self.get_logger().info("Motor Control Node Started")


    def gesture_callback(self, msg):

        gesture = msg.data

        self.get_logger().info(f"Received: {gesture}")

        if gesture == "FORWARD":
            forward()

        elif gesture == "BACKWARD":
            backward()

        elif gesture == "STOP":
            stop()

        # else:
        #     stop()
        else:
           print("Unknown command")
           stop()
        


def main(args=None):

    rclpy.init(args=args)

    node = MotorControlNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()