import cv2
import socket
import struct

# host = '192.168.1.31'
host = "192.168.1.5"

port = 9994

cap = cv2.VideoCapture(0)

width = 320#176#320
height = 240#144#240

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(0)



while True:

    print("Waiting for connection...")
    connection, address = server_socket.accept()
    print("Connected ", address)

    while True:

        ret, frame = cap.read()



        # frame = cv2.resize(frame, (width, height))

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # cv2.imshow('frame', frame)

        data = cv2.imencode('.jpg', frame)[1].tobytes()

        try:
            connection.sendall(struct.pack("!i", len(data)) + data)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(e)
            break



cap.release()
connection.close()
server_socket.close()
