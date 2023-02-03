import cv2 as cv
import time
import socket
import base64

webcam = cv.VideoCapture(0)

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
# host_ip = '192.168.1.5.'#  socket.gethostbyname(host_name)
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9997
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)

# width = 640
# height = 480
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', client_addr)

    _, frame = webcam.read()
    image = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    encoded, buffer = cv.imencode('.jpg', image, [cv.IMWRITE_JPEG_QUALITY, 80])

    message = base64.b64encode(buffer)
    server_socket.sendto(message, client_addr)

    image = cv.putText(image, 'FPS: ' + str(fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv.imshow("Widok", image)

    key = cv.waitKey(1)
    if key == 27:
        server_socket.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1

webcam.release()
cv.DestroyAllWindows()
