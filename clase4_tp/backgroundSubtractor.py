import cv2 as cv
import numpy as np
import time as tm

slider_val = -100
slider_val_max = 100


def on_trackbar(val):
    global slider_val
    slider_val = val


cap = cv.VideoCapture("carsRt9_3.avi")
fgbg = cv.createBackgroundSubtractorMOG2(history=20, varThreshold=25, detectShadows=True)

while True:
    ret, frame = cap.read()
    cv.imshow("origin", frame)
    fgmask = fgbg.apply(frame)
    cv.imshow("fgmask", fgmask)
    tm.sleep(0.1)
    bgImg = fgbg.getBackgroundImage()
    cv.imshow("backgroundImage", bgImg)
    cv.createTrackbar("Trackbar", "fgbg2", slider_val, slider_val_max, on_trackbar)
    fgbg2 = cv.BackgroundSubtractor.apply(fgbg, bgImg, fgmask, slider_val/100)
    cv.imshow("fgbg2", fgbg2)

    if cv.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv.destroyAllWindows()
