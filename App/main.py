import socket
import struct

import cv2
import imutils


def capture_frame():
    while True:
        try:
            ret, frame = cap.read()
            fire_detection(frame)
            # send_frames(conn, frame)
        except Exception as e:
            print("Error in capture_frames:", e)
            break


def send_frame(frame, conn):

    data = cv2.imencode('.jpg', frame)[1].tobytes()
    conn.sendall(struct.pack("!i", len(data)) + data)


def fire_detection(frame):

    # TODO: frame resize()
    # frame = cv2.resize(frame, (176, 144))
    frame = imutils.resize(frame, width=240, height=160)
    frame = imutils.rotate_bound(frame, 90)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(gray, 1.3, 5)  # higher = faster

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print("Fire detected")
        # TODO: notify()
    # return frame




# TODO: if __name__ == '__main__':


fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
width = 320
height = 240

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

host = "192.168.1.5"
port = 9993
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)





while True:
    connection, address = server_socket.accept()

    while True:

        data = cv2.imencode('.jpg', frame)[1].tobytes()
        connection.sendall(struct.pack("!i", len(data)) + data)



    frame = fire_detection(frame)
    cv2.imshow("Webcam", frame)
    cv2.waitKey(1)

cap.release()
connection.close()
cv2.destroyAllWindows()



