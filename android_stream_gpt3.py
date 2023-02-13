import cv2
import socket
import struct

host = '192.168.1.31'
port = 9994

cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

# TODO: width = 320
# TODO height = 480


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(0)

connection, address = server_socket.accept()

while True:

    #TODO: socket in while

    ret, frame = cap.read()

    # TODO: frame = cv.resize(frame, (width, height))

    # TODO: firedetection resize 80x160?

    # TODO: 1. frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    data = cv2.imencode('.jpg', frame)[1].tobytes()
    connection.sendall(struct.pack("!i", len(data)) + data)

cap.release()
connection.close()
server_socket.close()