import numpy as np
import cv2 as cv

face_cascade = cv.CascadeClassifier('lbpcascade_frontalface.xml')

cap = cv.VideoCapture(0)

while True:

    _, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # draw rectangle
        # cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = frame[y:y + h, x:x + w]

        # draw eclipse
        center = (x + w // 2, y + h // 2)
        frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        roi_gray = gray[y:y + h, x:x + w]

    cv.imshow('face detection - lbp cascade', frame)

    keyboard = cv.waitKey(30)
    if keyboard & 0xFF == 27:
        break
cap.release()
cv.destroyAllWindows()
