from math import pi, sin
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
p = 17 # pin 17
t0 = time()
f = 0.2 # frequency in Hz
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 500) # create PWM object @ 100 Hz
try:
    pwm.start(0) # initiate PWM at 0% duty cycle
    while 1:
        t = time() - t0
        B = (sin(2*pi*0.2*t))**2
        dc = B * 100 # scale to 0-100
        pwm.ChangeDutyCycle(dc) # set duty cycle
except KeyboardInterrupt: # stop gracefully on ctrl-C
    print('\nExiting')

pwm.stop()
GPIO.cleanup()