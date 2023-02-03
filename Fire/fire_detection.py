import cv2 as cv
import numpy as np

webcam = cv.VideoCapture(0)

# width = 640
# height = 480

fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    _, frame = webcam.read()
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    blur = cv.GaussianBlur(frame, (15, 15), 0)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]

    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')

    mask = cv.inRange(hsv, lower, upper)

    output = cv.bitwise_and(frame, hsv, mask=mask)

    size = cv.countNonZero(mask)
    if int(size) > 15000:
        print("Ogien")

    if _ == False:
        break
    frame = cv.putText(frame, 'FPS: ' + str(fps), (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv.imshow("Widok", frame)

    key = cv.waitKey(1)
    if key == 27:
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

