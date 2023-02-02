import cv2 as cv
import time

webcam = cv.VideoCapture(0)

# width = 640
# height = 480
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:

    _, frame = webcam.read()
    # frame = cv.resize(frame, (width, height))
    # image = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    image = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    image = cv.putText(image, 'FPS: ' + str(fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv.imshow("Widok", image)
    # cv.imshow("Widok", frame)
    key = cv.waitKey(1)
    if key == 27:
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
            print(fps)
        except:
            pass
    cnt += 1

webcam.release()
cv.DestroyAllWindows()
