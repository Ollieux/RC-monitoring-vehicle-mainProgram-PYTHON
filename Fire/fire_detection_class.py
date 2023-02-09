import cv2
import numpy as np


# fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
# fire_cascade = cv2.CascadeClassifier("fire_detection.xml")
# fire_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'fire_detection.xml')
# fire_cascade = cv2.CascadeClassifier('~/Rpi-Repo/Fire/fire_detection.xml')
# fire_cascade = cv2.CascadeClassifier("~/Rpi-Repo/Fire/fire_detection.xml")
fire_cascade = cv2.CascadeClassifier("/home/Rpi-Repo/Fire/fire_detection.xml")

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("http://192.168.1.31:8081/")

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20),(x + w + 20, y + h + 20), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        print("fire is detected")

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.DestroyAllWindows()