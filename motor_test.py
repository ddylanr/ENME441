import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Pick these 4 pins for ULN2003 IN1–IN4
IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19

coil_pins = [IN1, IN2, IN3, IN4]

for pin in coil_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Half-step sequence for 28BYJ-48
seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

delay = 0.002  # 2 ms per step

def step_motor(steps):
    direction = 1 if steps > 0 else -1
    steps = abs(steps)

    index = 0
    for i in range(steps):
        for pin in range(4):
            GPIO.output(coil_pins[pin], seq[index][pin])

        index = (index + direction) % 8
        time.sleep(delay)

try:
    print("Rotating CW 1 full revolution...")
    step_motor(2048)   # 2048 steps ≈ 360°

    time.sleep(1)

    print("Rotating CCW 1 full revolution...")
    step_motor(-2048)

    print("Done.")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
