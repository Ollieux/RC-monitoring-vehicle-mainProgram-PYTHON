import base64
import pickle
import socket
import struct

import cv2
import numpy as np

# SENDING_PORT = 9986
# send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # client_socket.connect(("192.168.1.5", SENDING_PORT))
# send_socket.bind(("192.168.1.5", SENDING_PORT))


# Set up the socket for receiving data from the Android app


RECEIVING_PORT = 9987
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.connect(('192.168.1.5', RECEIVING_PORT))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = receive_socket.recv(4 * 1024)  # 4K
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += receive_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
receive_socket.close()
# while True:
#     # img_len = receive_socket.recv(16)
#     # # if len(img_len) == 0:
#     # #     break
#     #
#     # img_len = int.from_bytes(img_len, byteorder='big')
#     # img_bytes = b''
#     # while len(img_bytes) < img_len:
#     #     img_bytes += receive_socket.recv(4096)
#     #
#     # frame = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), 1)
#     # cv2.imshow('frame', frame)
#
#     data = receive_socket.recv(4096)
#
#     if not data:
#         break
#
#     frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
#     cv2.imshow('frame', frame)
#     cv2.waitKey(1)
