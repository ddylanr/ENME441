import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class Shifter:
    def __init__(self, serialPin, latchPin, clockPin):
        self.serialPin = serialPin
        self.latchPin = latchPin
        self.clockPin = clockPin

        # Set up GPIO pins
        GPIO.setup(self.serialPin, GPIO.OUT)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=0) # start latch & clock low
        GPIO.setup(self.clockPin, GPIO.OUT, initial=0)
        
    def __ping(self, p): # ping the clock or latch pin
        GPIO.output(p,1)
        time.sleep(0)
        GPIO.output(p,0)

    def shiftByte(self, b): # send a byte of data to the output
        for i in range(8):
            GPIO.output(self.serialPin, b & (1<<i))
            self.__ping(self.clockPin) # ping the clock pin to shift register data
        self.__ping(self.latchPin) # ping the latch pin to send register to output

class Bug:
    def __init__(self, timestep, x, isWrapOn, __shifter):
        self.timestep = timestep # time step in seconds
        self.x = x # current x position (0-7)
        self.isWrapOn = isWrapOn
        self.__shifter = __shifter