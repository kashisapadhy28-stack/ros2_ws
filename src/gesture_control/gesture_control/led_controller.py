import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from gpiozero import LED
from time import sleep
import threading

led = LED(17)


class LEDController(Node):

    def __init__(self):
        super().__init__('led_controller')

        self.subscription = self.create_subscription(
            String,
            '/gesture',
            self.callback,
            10
        )

        self.get_logger().info("LED Controller Started")

    def callback(self, msg):

        command = msg.data

        self.get_logger().info(f"Received: {command}")

        thread = threading.Thread(
            target=self.led_worker,
            args=(command,),
            daemon=True
        )

        thread.start()

    def led_worker(self, command):

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


def main(args=None):

    rclpy.init(args=args)

    node = LEDController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()