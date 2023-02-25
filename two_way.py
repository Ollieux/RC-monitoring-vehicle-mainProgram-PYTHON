import base64
import pickle
import cv2
import socket
import struct
import threading
import multiprocessing
import imutils

# width = 640#320#176#640###
# height = 480#240#144#480###


# Set up the socket for sending data to the Android app


SENDING_PORT = 9987
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.bind(('192.168.1.5', SENDING_PORT))
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('192.168.1.5', SENDING_PORT))


# Set up the socket for receiving data from the Android app
# RECEIVING_PORT = 9986
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("192.168.1.5", RECEIVING_PORT))


def send_data():
    # client_socket.listen(5)
    ## client_socket.setblocking(False)
    while True:
        # print("Waiting for send connection...")
        # connection, address = client_socket.accept()
        # print("Send Connected ", address)
        # receive_thread = threading.Thread(target=receive_data, )
        # receive_thread.start()
        # while True:
        if connection:
            cap = cv2.VideoCapture(0)
            while cap.isOpened():
                ret, frame = cap.read()
                frame = imutils.resize(frame, width=320)
                frame = imutils.rotate_bound(frame, angle=-90)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                connection.sendall(message)

                cv2.imshow('TRANSMITTING VIDEO', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    connection.close()
                    # break
            ## frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            #encoded, data = cv2.imencode('.jpg', frame)
            # data = cv2.imencode('.jpg', frame)[1].tobytes()
            # try:
                # connection.sendall(struct.pack("!i", len(data)) + data)

                ## connection.sendall(data.tobytes())
                ## connection.sendall(data)

            #except (ConnectionResetError, ConnectionAbortedError) as e:
                #print(e)
                # receive_thread.join()
                #break


def receive_data():
#     # server_socket.listen(5)
#     # server_socket.setblocking(False)
    # while True:
        # print("Waiting for receive connection...")
        # connection, address = server_socket.accept()
        # print("Receive Connected ", address)
        while True:
            data = (connection.recv(1024)).decode("utf-8")
            if not data:
                break
            print("data: ", data)


# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# client_socket.listen(5)
#server_socket.listen(5)

# client_socket.setblocking(False)
# server_socket.setblocking(0)

# send_thread = threading.Thread(target=send_data, )
# send_thread.start()

# receive_thread = threading.Thread(target=receive_data, )
# receive_thread.start()

# send_process = multiprocessing.Process(target=send_data, )
# send_process.start()
#
# receive_process = multiprocessing.Process(target=receive_data, )
# receive_process.start()


# send_thread.join()
# receive_thread.join()


# send_process.join()
# receive_process.join()

socket.listen(1)

while True:
    print("Waiting for connection...")
    connection, address = socket.accept()
    print("Connected ", address)

    send_thread = threading.Thread(target=send_data, )
    send_thread.start()

    print("end")

#         conn1, addr1 = client_socket.accept()
#         conn2, addr2 = server_socket.accept()
#         threading.Thread(target=send_data, args=(conn1)).start()
#         threading.Thread(target=handle_client, args=(conn2)).start()









# cap.release()


