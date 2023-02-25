import pickle
import socket
import struct
import threading
import cv2


def send_frames(conn, frame):
    try:
        frame = cv2.resize(frame, (320, 480))
        result, frame = cv2.imencode('.jpg', frame)
        data = pickle.dumps(frame, 0)
        size = len(data)
        conn.sendall(struct.pack(">L", size) + data)
    except Exception as e:
        print("Error in send_frames:", e)


def capture_frames(conn):
    while True:
        try:
            ret, frame = cap.read()
            send_frames(conn, frame)
        except Exception as e:
            print("Error in capture_frames:", e)
            break


def face_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


if __name__ == "__main__":
    face_cascade = cv2.CascadeClassifier('Fire/fire_detection.xml')
    cap = cv2.VideoCapture(0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8485))
    server_socket.listen()
    print("Waiting for a client to connect...")
    conn, address = server_socket.accept()
    print("Connected to client at", address)

    t1 = threading.Thread(target=capture_frames, args=(conn,))
    t2 = threading.Thread(target=face_detection, args=(frame,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    cap.release()
    server_socket.close()
    cv2.destroyAllWindows()

    # NON FUNCTIONAL