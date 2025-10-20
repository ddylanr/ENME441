import RPi.GPIO as GPIO
from shifter import Shifter
from bug import Bug

s = Shifter(23, 24, 25)                # Initialize shift register
b = Bug(s, timestep=0.05, x=3, isWrapOn=False)  # Create Bug object

try:
    b.start()                          # Start the “lightning bug”
except KeyboardInterrupt:
    b.stop()
    GPIO.cleanup()
