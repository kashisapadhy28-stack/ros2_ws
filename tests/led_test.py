from gpiozero import LED
from time import sleep

# GPIO17 = physical pin 11
led = LED(17)

print("Blinking LED... Press Ctrl+C to stop")

try:
    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)

except KeyboardInterrupt:
    print("Stopping...")