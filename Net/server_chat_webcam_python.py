import pickle
import socket
import struct
import threading
import sys
import cv2
import imutils
# --- functions ---



def recv_msg():
    while True:
        recv_msg = conn.recv(1024)
        if not recv_msg:
            break
        recv_msg = recv_msg.decode()
        print(recv_msg)

def send_frame():
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            frame = imutils.rotate_bound(frame, angle=-90)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            conn.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                conn.close()

# --- main ---

host = '192.168.1.5'
port = 9977

s = socket.socket()
s.bind((host, port))
s.listen(1)

print("Waiting for connections")
conn, addr = s.accept()

print("Client has connected")
conn.send("Welcome to the server".encode())

# thread has to start before other loop
t = threading.Thread(target=recv_msg, )
t.start()

t2 = threading.Thread(target=send_frame, )
t2.start()
# send_msg()