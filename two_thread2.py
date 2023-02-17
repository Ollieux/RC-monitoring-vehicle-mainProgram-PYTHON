import queue
import socket
import struct
import cv2
import imutils
import numpy as np
import threading


def face_detection(frame):
    # TODO: frame = cv2.resize(frame, (176, 144))
    frame = imutils.resize(frame, width=176, height=144)
    frame = imutils.rotate_bound(frame, 90)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flames = fire_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in flames:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print("fire detected")
    return frame


# def capture_frames(encode_param, frame_queue):
# def capture_frames(frame_queue):
def capture_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            # TODO: frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame_queue.put(frame)
        else:
            break
    cap.release()


# def send_frames(encode_param, frame_queue):
# def send_frames(frame_queue):
def send_frames():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.1.5", 9994))
    server_socket.listen(1)
    print("Waiting for a client to connect...")
    while True:
        connection, client_address = server_socket.accept()
    # print(a)
        while True:
            frame = frame_queue.get()
            # TODO: frame = cv2.resize(frame, (320, 240))
            frame = imutils.resize(frame, width=320, height=240)
            frame = imutils.rotate_bound(frame, 90)
            data = cv2.imencode('.jpg', frame)[1].tobytes()
            connection.sendall(struct.pack("!i", len(data)) + data)


if __name__ == '__main__':
    fire_cascade = cv2.CascadeClassifier("Fire/fire_detection.xml")
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    frame_queue = queue.Queue()
    a = 7;
    # t1 = threading.Thread(target=capture_frames, args=(encode_param, frame_queue))
    # t2 = threading.Thread(target=send_frames, args=(encode_param, frame_queue))
    # t1 = threading.Thread(target=capture_frames, args=(frame_queue))
    # t2 = threading.Thread(target=send_frames, args=(frame_queue))
    t1 = threading.Thread(target=capture_frames, )
    t2 = threading.Thread(target=send_frames, )
    t1.start()
    t2.start()
    while True:
        _frame = frame_queue.get()
        _frame = face_detection(_frame)
        cv2.imshow('Webcam', _frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
