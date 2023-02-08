import RPi.GPIO as GPIO
import time


def Init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)

    global enableRight
    global enableLeft

    enableRight = GPIO.PWM(27, 100)
    enableLeft = GPIO.PWM(17, 100)
    enableRight.start(0)
    enableLeft.start(0)
    time.sleep(1)


def Stop():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    enableRight.ChangeDutyCycle(0)
    enableLeft.ChangeDutyCycle(0)


def moveFrontRight(value):
    global enableRight
    global enableLeft
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    enableRight.ChangeDutyCycle(value)
    enableLeft.ChangeDutyCycle(75)
    time.sleep(0.01)


def moveFrontLeft(value):
    global enableRight
    global enableLeft
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(26, GPIO.LOW)
    enableRight.ChangeDutyCycle(75)
    enableLeft.ChangeDutyCycle(value)
    time.sleep(0.01)


def moveBackRight(value):
    global enableRight
    global enableLeft
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    enableRight.ChangeDutyCycle(value)
    enableLeft.ChangeDutyCycle(75)
    time.sleep(0.01)


def moveBackLeft(value):
    global enableRight
    global enableLeft
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    enableRight.ChangeDutyCycle(75)
    enableLeft.ChangeDutyCycle(value)
    time.sleep(0.01)


def Close():
    global enableRight
    global enableLeft
    enableRight.stop()
    enableLeft.stop()
    GPIO.output(13, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.cleanup()


while True:
    try:
        moveFrontRight(25)
        time.sleep(5)
        moveFrontLeft(25)
        time.sleep(5)
        moveBackRight(25)
        time.sleep(5)
        moveBackRight(25)
        time.sleep(5)
    except KeyboardInterrupt:
        Close()
