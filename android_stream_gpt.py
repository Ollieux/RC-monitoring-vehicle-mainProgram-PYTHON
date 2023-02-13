import cv2
import socket
import numpy as np

# Create a socket connection
server_socket = socket.socket()
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.31"
port = 12345
server_socket.bind((host, port))
# server_socket.listen(1)
server_socket.listen(5)
print("Waiting for a connection...")
connection, address = server_socket.accept()
print("Accepted connection from", address)

# OpenCV to capture video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Encode the frame as JPEG
    encoded, buffer = cv2.imencode(".jpg", frame)

    # Send the encoded frame over the socket connection
    connection.sendall(buffer.tobytes())

# Clean up the socket connection
cap.release()
connection.close()
