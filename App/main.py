import socket
import struct
import threading
import time
import serial
import cv2
import queue
import firebase_admin
import imutils
from firebase_admin import credentials, messaging




def send_notification(title, msg):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        token=registration_token,
    )
    #TODO: final out
    response = messaging.send(message)
    print('Successfully sent message:', response)

# def interpret_data():
#
#     #TODO: data = data_queue.get()
#     pass


def send_controls():

    arduino = serial.Serial(port='COM11', baudrate=115200)
    while True:
        data = data_queue.get()
        # data += '#'
        arduino.write(data.encode())


def receive_data():

    while True:
        try:
            # data = connection.recv(1024).decode("utf-8")
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

    while True:
        frame = send_frame_queue.get()
        try:
            data = cv2.imencode('.jpg', frame)[1].tobytes()
            connection.sendall(struct.pack("!i", len(data)) + data)
            # conn.sendall(struct.pack("!i", len(data)) + data)
        except Exception as e:
            print(e)
            # conn.close()
            break


def capture_frame():

    global capturing

    cap = cv2.VideoCapture(0)
    # cap.set(3, WIDTH)
    # cap.set(4, HEIGHT)
    ## cap.set(5, FPS)
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

            detect_frame_queue.put(frame)

        if connected:
            send_frame_queue.put(frame)

        #TODO: final out
        cv2.imshow("Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        #TODO:
        # if not running:
        #   break

    # except Exception as e:
        # print("Error in capture_frames:", e)
    cap.release()
        # break


def detect_fire():

    global detecting
    detecting = True
    #TODO:
    # while running
    while True:

        frame = detect_frame_queue.get()

        #TODO?:
        # imutils.resize(frame, (176, 144))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flames = fire_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in flames:

            # TODO: final out
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("fire detected")

            # TODONE: notify()
            global notified
            if not notified:

                notified = True
                threading.Thread(target=send_notification, args=("Warning", "fire detected")).start() #TODO: temp, mq?

        # TODO: final out
        cv2.imshow("Detect", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

#TODO:
# if __name__ == '__main__':



host = "192.168.1.5"
port = 9977
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

fire_cascade = cv2.CascadeClassifier("fire_detection.xml")

cred = credentials.Certificate('Notification/pushnotifcationtest-f5539-firebase-adminsdk-2ssjk-6ca36caa53.json')
firebase_admin.initialize_app(cred)

registration_token = 'epZx5w_RToGbXxrpEjeMXN:APA91bG2_S8rKS3enFhMq9oHwBoJt_XYn4nQEwZE3gCyb-EX-tyhR8DhgvVnjhL0fO5k0-c6ZxBagDMcv_h-iAUZWB5DEGRS9njP1ihvhH_zldBCow2_iCEmX2Rth2A0HzbJ-1R0y3Gj'

WIDTH = 320
HEIGHT = 240
FPS = 10
SIZE = 96

capturing = False
detecting = False
connected = False
notified = False
fire_occured = False
running = True

send_frame_queue = queue.Queue()
detect_frame_queue = queue.Queue()
data_queue = queue.Queue()

## capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread = threading.Thread(target=capture_frame, )
capture_thread.start()

#time.sleep(10)
while not capturing:
    print("wait for capturing")

fire_thread = threading.Thread(target=detect_fire, )
fire_thread.start()

controls_thread = threading.Thread(target=send_controls, )
controls_thread.start()


while True:
    try:
        connected = False
        print("Waiting for connection")
        connection, client_address = server_socket.accept()
        connected = True
        print(client_address, " connected")
        receive_thread = threading.Thread(target=receive_data, )
        receive_thread.start()
        # send_thread = threading.Thread(target=send_frame)
        # send_thread.start()
        receive_thread.join()
        # send_thread.join()
        print("end connection")

    except KeyboardInterrupt as e:
        print(e)
        running = False
        break


# fire_thread.join()
# capture_thread.join()

#TODO: pre final
# git checkout -b pc
# git merge main
# git checkout -b main
# TODOs final/final out