import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    color = ('b', 'g', 'r')

    for i, c in enumerate(color):
        hist = cv.calcHist(frame, [i], None, [256], [0, 256])
        plt.plot(hist, color=c)
        plt.xlim([0, 256])

    plt.show()

cv.destroyAllWindows()
