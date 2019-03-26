import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while 1:
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame, frame, mask=mask)

    # Draw a diagonal blue line with thickness of 5 px
    cv.line(mask,(0,0),(511,511),(255,0,0),5)

    pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv.polylines(mask,[pts],True,(0,255,255))

    # Draw text
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(res,'Reconocedor de azul',(10,500), font, 3,(255,255,255),2,cv.LINE_AA)

    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
