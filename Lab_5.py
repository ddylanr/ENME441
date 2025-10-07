from math import pi, sin
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
p17 = 17 # pin 17
p27 = 27 # pin 27
t0 = time()
f = 0.2 # frequency in Hz
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p17, 500) # create PWM object @ 500 Hz
PWM = GPIO.PWM(p27, 500) # create PWM object @ 500 Hz
try:
    pwm.start(0) # initiate PWM at 0% duty cycle
    while 1:
        t = time() - t0
        B = (sin(2*pi*0.2*t))**2
        b = (sin(2*pi*f*t - (pi/11)))**2
        dc1 = B * 100 # scale to 0-100
        dc2 = b * 100 # scale to 0-100
        pwm.ChangeDutyCycle(dc) # set duty cycle
        PWM.ChangeDutyCycle(dc2) # set duty cycle
except KeyboardInterrupt: # stop gracefully on ctrl-C
    print('\nExiting')

pwm.stop()
GPIO.cleanup()