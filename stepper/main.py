from time import sleep
import RPi.GPIO as GPIO

DIR = 26   # Direction GPIO Pin
STEP = 19  # Step GPIO Pin
SLEEP = 13
CW = True     # Clockwise Rotation
MICRO = 4  # micro stepping
SPR = (360/1.8) * MICRO   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(SLEEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay = .001 / MICRO

def turn(degrees, dir):
    GPIO.output(DIR, dir)
    GPIO.output(SLEEP,1)
    sleep(0.5)
    for x in range(int((degrees/360) * SPR)):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        print("Moved:" + str(x))
    GPIO.output(SLEEP,0)
while True:
    turn(1080, CW)
    CW = not CW
    sleep(2)
    turn(1080, CW)
    CW = not CW
    sleep(2)

GPIO.cleanup()
