import struct
import cv2
import numpy as np
import socket
import threading


def capture_frames(_connection):
    cap = cv2.VideoCapture(0)
    global frame
    while True:
        # global frame

        # ret, frame = cap.read()
        # frame = cv2.resize(frame, (80, 160))
        # ret, jpeg = cv2.imencode('.jpg', frame)
        # server_socket.sendall(jpeg.tobytes())

        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        data = cv2.imencode('.jpg', frame)[1].tobytes()
        _connection.sendall(struct.pack("!i", len(data)) + data)


def fire_detection():
    global frame
    # TODO: resize
    __frame = frame
    gray = cv2.cvtColor(__frame, cv2.COLOR_BGR2GRAY)
    flames = fire_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in flames:
        cv2.rectangle(__frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print("fire detected")
    return __frame


if __name__ == '__main__':
    global frame
    fire_cascade = cv2.CascadeClassifier("Fire/fire_detection.xml")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.1.5", 9999))
    server_socket.listen(1)

    connection, client_address = server_socket.accept()

    t1 = threading.Thread(target=capture_frames, args=(connection,))
    # t2 = threading.Thread(target=face_detection, args=(frame,))

    t1.start()
    # t2.start()

    # t1.join()
    # t2.join()

    while True:
        # global frame
        _frame = fire_detection()
        cv2.imshow("Webcam", _frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    server_socket.close()
    cv2.destroyAllWindows()

# NON FUNCTIONAL
