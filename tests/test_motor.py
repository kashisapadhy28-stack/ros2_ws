from gpiozero import OutputDevice
from time import sleep

# Left motor
in1 = OutputDevice(17)
in2 = OutputDevice(27)

# Right motor
in3 = OutputDevice(22)
in4 = OutputDevice(23)

def forward():
    print("Forward")
    in1.on()
    in2.off()

    in3.on()
    in4.off()

def backward():
    print("Backward")
    in1.off()
    in2.on()

    in3.off()
    in4.on()

def stop():
    print("Stop")
    in1.off()
    in2.off()

    in3.off()
    in4.off()

forward()
sleep(3)

stop()
sleep(2)

backward()
sleep(3)

stop()