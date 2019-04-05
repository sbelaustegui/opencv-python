import cv2 as cv

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    yuv = cv.cvtColor(frame, cv.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    yuv[:,:,0] = cv.equalizeHist(yuv[:,:,0])

    # convert the YUV image back to RGB format
    img_output = cv.cvtColor(yuv, cv.COLOR_YUV2BGR)

    cv.imshow('frame',img_output)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()
