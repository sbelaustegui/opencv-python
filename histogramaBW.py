import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
while 1:

    _, frame = cap.read()

    hist = cv.calcHist(frame, [0], None, [256], [0, 256])
    plt.plot(hist, color='gray' )

    plt.xlabel('intensidad de iluminacion')
    plt.ylabel('cantidad de pixeles')
    plt.show()


cv.destroyAllWindows()
