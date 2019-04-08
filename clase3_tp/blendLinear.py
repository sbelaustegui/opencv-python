import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    grey = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    # Read the images
    background = cv.imread("blue.png")

    # Convert uint8 to float
    foreground = frame.astype(float)
    background = background.astype(float)

    # Normalize the alpha mask to keep intensity between 0 and 1
    alpha = grey.astype(float)/255

    # Multiply the foreground with the alpha matte
    foreground = cv.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv.multiply(1.0 - alpha, background)

    # Add the masked foreground and background.
    outImage = cv.add(foreground, background)

    # Display image
    cv.imshow("outImg", outImage/255)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()
