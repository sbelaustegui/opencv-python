# invert = cv.invertAffineTransform(matrix, matrix)
# invert_result = cv.warpAffine(img, invert, (cols, rows))
# cv.imshow("invert", invert_result)

#  Comparar dos fotos de un plano (un pizarron, una pared) obtenidas desde distinto punto de vista,
#  pedir al usuario hacer clic en 4 puntos correspondientes,
#  computar la transformacion de perspectiva y aplicarlas sobre ambas imagenes.

import cv2 as cv
import numpy as np

img1 = cv.imread("whiteboard1.jpg")
img2 = cv.imread("whiteboard2.jpg")
rows, cols, ch = img1.shape

scale_percent = 15  # escalar el porcentaje
width = int(img1.shape[1] * scale_percent / 100)  # col = width
height = int(img1.shape[0] * scale_percent / 100)  # row = height
dim = (width, height)

# resize images
resized = cv.resize(img1, dim, interpolation=cv.INTER_AREA)
resized2 = cv.resize(img2, dim, interpolation=cv.INTER_AREA)
cv.imshow("whiteboard 1", resized)
cv.imshow("whiteboard 2", resized2)

posList = []


# read 4 inputs and draw circles
def draw_circle(event, x, y, flags, param):
   global posList, posNp
   if event == cv.EVENT_LBUTTONDOWN:
        if len(posList) <= 3:
            cv.circle(resized, (x, y), 5, (0, 0, 255), -1)
            cv.circle(resized2, (x, y), 5, (0, 0, 255), -1)
            posList.append((x, y))
            print posList
            cv.imshow("whiteboard 1", resized)
            cv.imshow("whiteboard 2", resized2)
            posNp = np.float32(posList)  # convert to numpy for other usages
        elif len(posList) == 4:
            # first point = top-left
            # second point = top-right
            # third point = bottom-left
            # fourth point = bottom-right
            dist = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  # points ser to corner
            new_matrix = cv.getPerspectiveTransform(posNp, dist)
            result1 = cv.warpPerspective(resized, new_matrix, (width, height))
            result2 = cv.warpPerspective(resized2, new_matrix, (width, height))
            cv.imshow("whiteboard 1", result1)
            cv.imshow("whiteboard 2", result2)


while True:
    # solo se dibuja en 1er imagen
    cv.setMouseCallback('whiteboard 1', draw_circle)
    if cv.waitKey(0) == 27:
        break
cv.destroyAllWindows()
