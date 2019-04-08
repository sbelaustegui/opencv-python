import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    grey = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    th, im_th = cv.threshold(grey, 200, 255, cv.THRESH_BINARY);

    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv.floodFill(im_floodfill, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    fill_image = im_th | im_floodfill_inv

    cv.imshow('frame',fill_image)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break


cv.destroyAllWindows()
