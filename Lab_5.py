from math import pi, sin
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin_outs = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5]
t0 = time()
f = 0.2 # frequency in Hz
step = pi/11 # phase step

pins = []
for pin in pin_outs:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 500) # create PWM object @ 500 Hz
    pwm.start(0) # start PWM with 0% duty cycle
    pins.append(pwm)

try:
    while 1:
        t = time() - t0
        for i in range(len(pins)):
            # calculate duty cycle
            B = (sin(2*pi*0.2*t - i*(pi/11)))**2  # Removed '- (p)' since 'p' is undefined
            dc = B * 100 # scale to 0-100
            pwm.ChangeDutyCycle(dc) # set duty cycle        
            
except KeyboardInterrupt: # stop gracefully on ctrl-C
    print('\nExiting')

pwm.stop()
GPIO.cleanup()