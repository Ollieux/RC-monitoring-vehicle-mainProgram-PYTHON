import RPi.GPIO as GPIO
import time
from socket import *


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


# def moveForward(value):
#     global enableRight
#     global enableLeft
#     GPIO.output(5, GPIO.LOW)
#     GPIO.output(6, GPIO.HIGH)
#     GPIO.output(13, GPIO.HIGH)
#     GPIO.output(26, GPIO.LOW)
#     enableRight.ChangeDutyCycle(35)
#     enableLeft.ChangeDutyCycle(35)
#     time.sleep(0.01)
#
#
# def moveBackward(value):
#     global enableRight
#     global enableLeft
#     GPIO.output(5, GPIO.HIGH)
#     GPIO.output(6, GPIO.LOW)
#     GPIO.output(13, GPIO.LOW)
#     GPIO.output(26, GPIO.HIGH)
#     enableRight.ChangeDutyCycle(35)
#     enableLeft.ChangeDutyCycle(35)
#     time.sleep(0.01)


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


# def moveRight(value):
#     global enableRight
#     global enableLeft
#     GPIO.output(5, GPIO.HIGH)
#     GPIO.output(6, GPIO.LOW)
#     GPIO.output(13, GPIO.HIGH)
#     GPIO.output(26, GPIO.LOW)
#     enableRight.ChangeDutyCycle(35)
#     enableLeft.ChangeDutyCycle(35)
#     time.sleep(0.01)


# def moveLeft(value):
#     global enableRight
#     global enableLeft
#     GPIO.output(5, GPIO.LOW)
#     GPIO.output(6, GPIO.HIGH)
#     GPIO.output(13, GPIO.LOW)
#     GPIO.output(26, GPIO.HIGH)
#     enableRight.ChangeDutyCycle(35)
#     enableLeft.ChangeDutyCycle(35)
#     time.sleep(0.01)


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


host = ''
port = 21567
size = 1024
addr = (host, port)
Init()
print("Initialization completed")
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(addr)
tcpSerSock.listen(5)
print("Program starts")

while True:

    tcpCliSock, ad = tcpSerSock.accept()
    try:
        while True:
            data = (tcpCliSock.recv(size)).decode("utf-8")
            print(data == "null")
            print(data)
            if not data:
                break
            else:
                if data == "null":
                    Stop()
                else:
                    try:
                        data = int(data)
                    except:
                        break

                    if 0 < data < 90:

                        value = int((data / 90) * 75)
                        moveFrontRight(value)
                        print("rightUP " + str(value))

                    elif 90 < data < 180:

                        value = int(((90 - (data - 90)) / 90) * 75)
                        moveFrontLeft(value)
                        print("leftUP " + str(value))

                    elif 180 < data < 270:

                        value = int(((data - 180) / 90) * 75)
                        moveBackLeft(value)
                        print("leftDOWN " + str(value))

                    elif 270 < data < 360:

                        value = int(((90 - (data - 270)) / 90) * 75)
                        moveBackRight(value)
                        print("rightDOWN " + str(value))

                    elif data == 0:

                        # robot.rightUp(0)
                        moveFrontRight(0)

                    elif data == 90:

                        moveFrontRight(75)

                    elif data == 180:

                        moveBackLeft(0)

                    elif data == 270:

                        moveBackRight(75)

    except KeyboardInterrupt:
        Close()

tcpSerSock.close()
