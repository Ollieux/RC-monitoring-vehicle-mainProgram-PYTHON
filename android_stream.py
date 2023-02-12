# from numpy.core import numeric
# import requests
import cv2
# import pickle
import socket
# import struct
# import numpy as np
import imutils
import base64
# from pyzbar import pyzbar


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vid = cv2.VideoCapture(0)
    host_ip = "192.168.1.31"
    print('IP DEL HOST:', host_ip)
    port = 9999
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)

    server_socket.listen(5)
    print("LUGAR DE ESCUCHA: ", socket_address)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print('CONEXIÓN ENTRANTE:', addr)
            WIDTH = 400
            while True:
                try:
                    _,img = vid.read()
                    frame = imutils.resize(img, width=WIDTH)
                    #read_barcodes(frame)
                    cv2.imshow("Android_cam", frame)
                    encoded,buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                    message = base64.b64encode(buffer)
                    size = len(message)
                    print(size)
                    strSize = str(size) + "\n"
                    client_socket.sendto(strSize.encode('utf-8'),addr)
                    client_socket.sendto(message,addr)

                    client_socket.sendto(("\nhappy face\n").encode('utf-8'),addr)
                except Exception as e:
                    print(e)
                    raise Exception(e)
                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()
    except KeyboardInterrupt:
        print('Finalizado')

