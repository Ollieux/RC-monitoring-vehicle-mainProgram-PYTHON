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


# detect_fire_run = False

def send_notification(title, msg):
    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

def interpret_data():
    #TODO: data = data_queue.get()
    pass

def send_controls():
    # arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    while True:
        # if not data_queue.empty():
            # data = data_queue.get()
            # arduino.write(data + '\n')
            pass

def receive_data():
    while True:
        data = connection.recv(1024).decode("utf-8")
        if not data:
            print("null")
            break
        # data = data.decode().decode("utf-8")
        # values = data.split(',')
        # values = [int(x) for x in data.split(',')]
        # print(values)
        print(data)
        #TODO:
        #   data_queue.put(data)


def send_frame(): # conn):
    while True:
        #TODONE: if not frame_queue.empty():
        if not frame_queue.empty():
            __frame = frame_queue.get()
            # if __frame:
            try:
                data = cv2.imencode('.jpg', __frame)[1].tobytes()
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
    #TODO:
    cap.set(5, FPS)
    # while True:
        # try:
    capturing = True
    while cap.isOpened():

        ret, frame = cap.read()

        # TODO: tutaj rotate, a jak tak to imutils czy cv
        #frame = imutils.resize(frame, width=320)
        # frame = imutils.rotate_bound(frame, angle=-90)

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # if detecting:
        #     frame_queue.put(frame)
        # else:
        #     # fire_thread = threading.Thread(target=detect_fire, )
        #     # fire_thread.start()
        #     pass

        # if connected:
        #     frame_queue.put(frame)

        frame_queue.put(frame)


        cv2.imshow("Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # except Exception as e:
        # print("Error in capture_frames:", e)
    cap.release()
    # break


def detect_fire():

    global detecting
    detecting = True
    while True:
        if not frame_queue.empty():
            # print("queue: ", frame_queue.qsize())
            _frame = frame_queue.get()
        # if _frame:

            #TODO: imutils.resize(_frame, (176, 144))

            gray = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)
            flames = fire_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in flames:
                cv2.rectangle(_frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #TODO: rpi out
                print("fire detected")
                # TODONE: notify()
                global notified
                if not notified:
                    notified = True
                    threading.Thread(target=send_notification, args=("Warning", "fire detected")).start() #TODO: temp, mq?
            cv2.imshow("Detect", _frame) #TODO: rpi out
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        else:
            # detecting = False
            # print("Cannot detect")
            # break
            pass

        #return frame

# if __name__ == '__main__':




host = "192.168.1.31"
# host = "192.168.1.5"
port = 9977
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
# server_socket.listen(5)
server_socket.listen(1)

# fire_cascade = cv2.CascadeClassifier("Fire/fire_detection.xml")
fire_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'fire_detection.xml')


# cred = credentials.Certificate('Notification/pushnotifcationtest-f5539-firebase-adminsdk-2ssjk-6ca36caa53.json')
cred = credentials.Certificate('/home/rpi/Rpi-Repo/Notification/pushnotifcationtest-f5539-firebase-adminsdk-2ssjk-6ca36caa53.json')
firebase_admin.initialize_app(cred)

registration_token = 'epZx5w_RToGbXxrpEjeMXN:APA91bG2_S8rKS3enFhMq9oHwBoJt_XYn4nQEwZE3gCyb-EX-tyhR8DhgvVnjhL0fO5k0-c6ZxBagDMcv_h-iAUZWB5DEGRS9njP1ihvhH_zldBCow2_iCEmX2Rth2A0HzbJ-1R0y3Gj'

WIDTH = 320
HEIGHT = 240
FPS = 10

capturing = False
detecting = False
connected = False
notified = False
fire_occured = False
frame_queue = queue.Queue()
# data_queue = queue.Queue()

# capture_thread = threading.Thread(target=capture_frame, daemon=True)
capture_thread = threading.Thread(target=capture_frame, )
capture_thread.start()

#time.sleep(10)
while not capturing:
    print("wait for capturing")

fire_thread = threading.Thread(target=detect_fire, )
fire_thread.start()

# controls_thread = threading.Thread(target=send_controls, )
# controls_thread.start


while True:
    try:
        connected = False
        print("Waiting for connection")
        connection, client_address = server_socket.accept()
        connected = True
        print(client_address, " connected")
        receive_thread = threading.Thread(target=receive_data, )
        receive_thread.start()
        send_thread = threading.Thread(target=send_frame, )
        send_thread.start()
        # threading.Thread(target=send_frame, args=connection).start()
        receive_thread.join()
        send_thread.join()
        print("end connection")

    except KeyboardInterrupt as e:
        print(e)
        break


# fire_thread.join()
# capture_thread.join()




