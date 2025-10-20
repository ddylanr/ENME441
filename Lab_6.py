import random
import RPi.GPIO as GPIO
import time
from shifter import Shifter

s = Shifter(23, 24, 25)  # Initialize shifter with data, latch, clock pins

try:
    position = 0  # start with leftmost LED (bit 0)

    while True:
        # Create the 8-bit pattern with one LED on
        pattern = 1 << position
        s.shiftByte(pattern)

        time.sleep(0.05)

        # Randomly move left (-1) or right (+1)
        step = random.choice([-1, 1])
        position += step

        # Prevent going out of bounds (0–7)
        if position < 0:
            position = 0
        elif position > 7:
            position = 7

except KeyboardInterrupt:
    GPIO.cleanup()