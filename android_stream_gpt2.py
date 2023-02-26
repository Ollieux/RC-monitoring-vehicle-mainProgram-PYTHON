import cv2
import numpy as np
import socket
import struct

host = "192.168.1.31"
port = 12346

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(0)

connection, address = server_socket.accept()
connection = connection.makefile("rb")

cam = cv2.VideoCapture(0)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encimg = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(encimg)
    stringData = data.tobytes()

    connection.write(struct.pack("<L", len(stringData)) + stringData)

cam.release()
cv2.destroyAllWindows()


# send data 2