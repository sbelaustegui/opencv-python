import cv2 as cv

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    grey = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    eq = cv.equalizeHist(grey)

    cv.imshow('frame',eq)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()
