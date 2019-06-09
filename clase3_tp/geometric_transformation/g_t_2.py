# Comparar dos fotos de la misma escena una girada respecto de la otra,
#  pedir al usuario hacer clic en 3 puntos correspondientes,
#  computar la transformacion afin y aplicarla sobre ambas imagenes.
#  Deberia obtenerse una aproximacion de la otra.

import cv2 as cv
import numpy as np

img = cv.imread("painting.jpg")
rows, cols, ch = img.shape
matrix = cv.getRotationMatrix2D((cols / 2, rows / 2), 45, 1)
img2 = cv.warpAffine(img, matrix, (cols, rows))
cv.imshow("image", img)
cv.imshow("image2", img2)
distList = []


# read 3 inputs and draw circles
def draw_circle(event, x, y, flags, param):
   global distList, dist
   if event == cv.EVENT_LBUTTONDOWN:
        if len(distList) <= 2:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)
            cv.circle(img2, (x, y), 5, (0, 0, 255), -1)
            distList.append((x, y))
            print(distList)
            cv.imshow("image", img)
            cv.imshow("image2", img2)
            dist = np.float32(distList)  # convert to numpy for other usages
        elif len(distList) == 3:
            # first point = top-left
            # second point = top-right
            # third point = bottom-left
            posNp = np.float32([[0, 0], [cols, 0], [0, rows]])  # points set to corners
            new_matrix = cv.getAffineTransform(dist, posNp)
            # new_matrix = cv.getAffineTransform(posNp, dist)
            result1 = cv.warpAffine(img, new_matrix, (cols, rows))
            result2 = cv.warpAffine(img2, new_matrix, (cols, rows))
            cv.imshow("image", result1)
            cv.imshow("image2", result2)


while True:
    # posList = []
    cv.setMouseCallback('image', draw_circle)
    if cv.waitKey(0) == 27:
        break
cv.destroyAllWindows()




