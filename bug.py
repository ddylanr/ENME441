import RPi.GPIO as GPIO
import time
from shifter import Shifter, Bug

# Pin setup
dataPin, latchPin, clockPin = 23, 24, 25
s1, s2, s3 = 17, 27, 22  # example input pins

GPIO.setmode(GPIO.BCM)
for pin in [s1, s2, s3]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create objects
s = Shifter(dataPin, latchPin, clockPin)
bug = Bug(s)

last_s2 = GPIO.input(s2)

try:
    while True:
        # a. Turn bug on/off with s1
        bug.on = GPIO.input(s1) == GPIO.HIGH

        # b. Flip wrapping when s2 changes state
        s2_state = GPIO.input(s2)
        if s2_state != last_s2:
            bug.wrap = not bug.wrap
            last_s2 = s2_state

        # c. Speed up when s3 is on
        bug.speed = 0.05 / 3 if GPIO.input(s3) == GPIO.HIGH else 0.05

        # move if on
        bug.move()

except KeyboardInterrupt:
    GPIO.cleanup()
