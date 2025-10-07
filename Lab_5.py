from math import pi, sin
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
p1 = 17 # pin 17
p2 = 27 # pin 27
t0 = time()
f = 0.2 # frequency in Hz
GPIO.setup(p1, GPIO.OUT)
GPIO.setup(p2, GPIO.OUT)


pwm1 = GPIO.PWM(p1, 500) # create PWM object @ 500 Hz
pwm2 = GPIO.PWM(p2, 500) # create PWM object @ 500 Hz
try:
    pwm1.start(0) # initiate PWM at 0% duty cycle
    pwm2.start(0) # initiate PWM at 0% duty cycle
    while 1:
        t = time() - t0
        B = (sin(2*pi*0.2*t))**2
        b = (sin(2*pi*f*t - (pi/11)))**2
        dc1 = B * 100 # scale to 0-100
        dc2 = b * 100 # scale to 0-100
        pwm1.ChangeDutyCycle(dc1) # set duty cycle
        pwm2.ChangeDutyCycle(dc2) # set duty cycle
except KeyboardInterrupt: # stop gracefully on ctrl-C
    print('\nExiting')

pwm1.stop()
pwm2.stop()
GPIO.cleanup()