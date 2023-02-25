import pickle
import socket
import struct
import threading
import cv2
import sys



# --- functions ---

def recv_frame():
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = s.recv(4 * 1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += s.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def send_msg():
    while True:
        send_msg = input(str("Enter message: "))
        send_msg = send_msg.encode()
        s.send(send_msg)
        print("Message sent")

# --- main ---

host = '192.168.1.5'
port = 9977

s = socket.socket()
s.connect((host, port))

print("Connected to the server")

message = s.recv(1024)
message = message.decode()
print(message)



# thread has to start before other loop
t = threading.Thread(target=recv_frame)
t.start()


t2 = threading.Thread(target=send_msg, )
t2.start()
# send_msg()