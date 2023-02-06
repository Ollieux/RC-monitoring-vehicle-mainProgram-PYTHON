import cv2 as cv

# webcam = cv.VideoCapture(0)
webcam = cv.VideoCapture("http://192.168.1.31:8081/")

# width = 640
# height = 480

while True:
    _, frame = webcam.read()
    # frame = cv.resize(frame, (width, height))
    # image = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    image = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    cv.imshow("Widok", image)
    # cv.imshow("Widok", frame)
    key = cv.waitKey(1)
    if key == 27:
        break

webcam.release()
cv.DestroyAllWindows()
