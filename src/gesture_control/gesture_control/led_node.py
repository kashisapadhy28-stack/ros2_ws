import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from gpiozero import LED

class LEDNode(Node):
    def __init__(self):
        super().__init__('led_node')

        self.led = LED(17)

        self.subscription = self.create_subscription(
            String,
            '/gesture',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        gesture = msg.data
        self.get_logger().info(f"Gesture: {gesture}")

        if gesture == "thumbs_up":
            self.led.on()

        elif gesture == "thumbs_down":
            self.led.off()

def main(args=None):
    rclpy.init(args=args)
    node = LEDNode()
    rclpy.spin(node)
    rclpy.shutdown()
