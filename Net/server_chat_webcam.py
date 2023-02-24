import pickle
import socket
import struct
import threading
import cv2
import imutils
# --- functions ---



def recive_data():
    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            print("null")
            break
        # data = data.decode().decode("utf-8")
        # values = data.split(',')
        # values = [int(x) for x in data.split(',')]
        # print(values)
        print(data)

def send_frame():
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            ret, frame = vid.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            #TODO: imutils.resize() ?
            data = cv2.imencode('.jpg', frame)[1].tobytes()
            try:

                conn.sendall(struct.pack("!i", len(data)) + data)
            except Exception as e:
                print(e)
                break
            # frame = imutils.resize(frame, width=320)
            # frame = imutils.rotate_bound(frame, angle=-90)
            # a = pickle.dumps(frame)
            # message = struct.pack("Q", len(a)) + a
            # conn.sendall(message)
            #

            # cv2.imshow('TRANSMITTING VIDEO', frame)
            # key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
            #     conn.close()

# --- main ---

host = '192.168.1.5'
port = 9977

s = socket.socket()
s.bind((host, port))
s.listen(1)

# while True:
print("Waiting for connection...")
conn, addr = s.accept()
print(addr, " connected")

    # t
    #receive_thread = threading.Thread(target=recive_data, daemon=True)
receive_thread = threading.Thread(target=recive_data, )
receive_thread.start()

    # t2
    #send_thread = threading.Thread(target=send_frame, daemon=True)
send_thread = threading.Thread(target=send_frame)
send_thread.start()

receive_thread.join()
send_thread.join()




# send_thread = threading.Thread(target=send_frame, )
# send_thread.start()
# receive_thread = threading.Thread(target=recive_data, )
# receive_thread.start()
# send_thread.join()
# receive_thread.join()


print("end")
