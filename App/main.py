import os
import socket
import struct
import threading
import time
import serial
import cv2
import queue
import firebase_admin
import imutils
import RPi.GPIO as GPIO
import w1thermsensor
from firebase_admin import credentials, messaging




def send_notification(factor, _):

    title = "Warning!"
    temperature = sensor.get_temperature()

    if factor == "fire":
        message = "fire detected, temperature: " + str(temperature) + "*C"

    elif factor == "smoke":

        message = "smoke detected, temperature: " + str(temperature) + "*C"

    else:
        message = ""

    msg = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message
        ),
        token=registration_token,
    )
    #TODO: final out
    response = messaging.send(msg)
    print('Successfully sent message:', response)

def button_callback(channel):

    print("Button was pushed!")
    os.system("sudo reboot")

def send_controls():

    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

    while True:
        data = data_queue.get()
        # data += '#'
        arduino.write(data.encode())


def receive_data():

    while True:
        try:
            data = connection.recv(SIZE).decode("utf-8")
            if not data:
                print("null")
                break
            print(data)
            data_queue.put(data)
        except Exception as e:
            print(e)
            break


def send_frame():

    global gtemperature
    temp = gtemperature

    while True:
        sframe = send_frame_queue.get()

        try:
            temp = temp_queue.get(block=False)

        except queue.Empty:
            pass

        finally:
            gtemperature = temp

        sframe = cv2.putText(sframe, 'temp: ' + str(temp) + '*C', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        try:
            data = cv2.imencode('.jpg', sframe)[1].tobytes()
            connection.sendall(struct.pack("!i", len(data)) + data)
            # conn.sendall(struct.pack("!i", len(data)) + data)
        except Exception as e:
            print(e)
            # conn.close()
            break


def capture_frame():

    global capturing

    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)
    cap.set(5, FPS)
    # while True:
        # try:
    capturing = True
    while cap.isOpened():

        ret, frame = cap.read()

        #TODO?: tutaj resize imutils/cv
        # frame = imutils.resize(frame, (width=WIDTH, height=HEIGHT)) #
        # frame = cv2.rotate(frame, (width=WIDTH, height=HEIGHT)) ##
        # moze sie klocic z podwojnym resizem w przypadku koniecznosci resize dla detect


        #TODO?: tutaj rotate, imutils/cv
        # frame = imutils.rotate_bound(frame, angle=-90)

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if detecting:

            #TODO?: tutaj resize dla detect
            # imutils.resize(frame, (width=176, height=144))
            # frame = cv2.resize(frame, (176, 144))

            detect_frame_queue.put(frame)

        if connected:

            send_frame_queue.put(frame)

        #TODO: final out
        cv2.imshow("Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        if not running:
            break

    # except Exception as e:
        # print("Error in capture_frames:", e)
    capturing = False
    cap.release()
        # break


def detect_smoke():

    while True:

        # if not GPIO.input(5):
        if not GPIO.input(18):

            global smoke_notified, smoke_time

            if smoke_notified:

                if time.time() - smoke_time > NOTIFICATION_TIMER:
                    smoke_notified = False

            if not smoke_notified:

                threading.Thread(target=send_notification, args=("smoke", "")).start()
                smoke_time = time.time()
                smoke_notified = True


        time.sleep(1)


def detect_fire():

    global detecting
    detecting = True
    while running:

        dframe = detect_frame_queue.get()

        gray = cv2.cvtColor(dframe, cv2.COLOR_BGR2GRAY)
        flames = fire_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in flames:

            # TODO: final out
            cv2.rectangle(dframe, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("fire detected")

            global fire_notified, fire_time

            if fire_notified:

                # if not time.time() - fire_time > FIRE_TIMER:
                if time.time() - fire_time > NOTIFICATION_TIMER:
                    fire_notified = False
                    # break

            # fire_notified = False

            if not fire_notified:

                threading.Thread(target=send_notification, args=("fire", "")).start()
                fire_time = time.time()
                fire_notified = True

        # TODO: final out
        cv2.imshow("Detect", dframe)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            detecting = False
            break

def read_temp():

    while connected:
        read = sensor.get_temperature()
        temp_queue.put(read)
        time.sleep(1)



def button_callback(channel):
    print("Button was pushed!")
    GPIO.cleanup();
    os.system("sudo reboot")

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)  # BCM numbering, not BOARD
# GPIO.setup(5, GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(17, GPIO.RISING, callback=button_callback)
# GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

sensor = w1thermsensor.W1ThermSensor()

host = socket.gethostbyname(socket.gethostname() + ".local")
#TODO:
# final out
print("IP address of the localhost is {}".format(host))

port = 9977
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

fire_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'fire_detection.xml')

cred = credentials.Certificate('/home/rpi/Rpi-Repo/Notification/pushnotifcationtest-f5539-firebase-adminsdk-2ssjk-6ca36caa53.json')
firebase_admin.initialize_app(cred)

registration_token = 'epZx5w_RToGbXxrpEjeMXN:APA91bG2_S8rKS3enFhMq9oHwBoJt_XYn4nQEwZE3gCyb-EX-tyhR8DhgvVnjhL0fO5k0-c6ZxBagDMcv_h-iAUZWB5DEGRS9njP1ihvhH_zldBCow2_iCEmX2Rth2A0HzbJ-1R0y3Gj'

WIDTH = 320
HEIGHT = 240
FPS = 10
SIZE = 96 # 1024
NOTIFICATION_TIMER = 30 #300

capturing = False
detecting = False
connected = False
fire_notified = False
smoke_notified = False
fire_time = 0
smoke_time = 0
gtemperature = 0 # sensor.get_temperature()
running = True

send_frame_queue = queue.Queue()
detect_frame_queue = queue.Queue()
data_queue = queue.Queue()
temp_queue = queue.Queue()

## capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread = threading.Thread(target=capture_frame, )
capture_thread.start()


#time.sleep(10)
#TODO: final out
print("wait for capturing")

while not capturing:
    
    pass


fire_thread = threading.Thread(target=detect_fire, )
fire_thread.start()

controls_thread = threading.Thread(target=send_controls, )
controls_thread.start()

# smoke_thread = threading.Thread(target=detect_smoke, )
# smoke_thread.start()

temp_thread = threading.Thread(target=read_temp, )
temp_thread.start()


while True:
    try:
        print("Waiting for connection")
        connection, client_address = server_socket.accept()
        connected = True
        print(client_address, " connected")
        receive_thread = threading.Thread(target=receive_data, )
        receive_thread.start()
        send_thread = threading.Thread(target=send_frame, )
        send_thread.start()
        #TODO: if not capturing:
        # backup_capture_thread = threading.Thread(target=capture_frame, )
        # backup_capture_thread.start()
        receive_thread.join()
        send_thread.join()
        print("end connection")
        connected = False

    except KeyboardInterrupt as e:
        print(e)
        running = False
        GPIO.cleanup()
        break


## fire_thread.join()
## capture_thread.join()

#TODO: pre final
# git checkout -b pc
# git merge main
# git checkout main
# git merge dev-rpi
# TODOs final/final out