from math import pi, sin
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin_outs = [17, 27, 22, 10, 9, 11, 5, 6, 13, 19]
button = 26
t0 = time()
f = 0.2 # frequency in Hz
step = pi/11 # phase step
step_sign = 1 # direction of wave

pins = []
for pin in pin_outs:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 500) # create PWM object @ 500 Hz
    pwm.start(0) # start PWM with 0% duty cycle
    pins.append(pwm)

def button_pressed(channel):
    global step_sign
    step_sign *= -1

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button, GPIO.RISING, callback=button_pressed, bouncetime=200)

try:
    while 1:
        t = time() - t0
        for i in range(len(pins)):
            # calculate duty cycle
            B = (sin(2*pi*f*t - i*step_sign*step))**2
            dc = B * 100 # scale to 0-100
            pins[i].ChangeDutyCycle(dc) # set duty cycle 

            
except KeyboardInterrupt: # stop gracefully on ctrl-C
    print('\nExiting')

for pwm in pins:
    pwm.stop()
GPIO.cleanup()