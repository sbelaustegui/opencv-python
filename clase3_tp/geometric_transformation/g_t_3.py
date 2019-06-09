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

posList1 = []
posList2 = []

# first point = top-left
# second point = top-right
# third point = bottom-left
# fourth point = bottom-right
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)]


# read 4 inputs and draw circles
def draw_circle1(event, x, y, flags, param):
   global posList1, posNp1
   if event == cv.EVENT_LBUTTONDOWN:
        if len(posList1) != 4:
            cv.circle(resized, (x, y), 5, colors[len(posList1)], -1)
            posList1.append((x, y))
            print(posList1)
            cv.imshow("whiteboard 1", resized)
            posNp1 = np.float32(posList1)  # convert to numpy for other usages
        else:
            return


def draw_circle2(event, x, y, flags, param):
   global posNp2, posList2
   if event == cv.EVENT_LBUTTONDOWN:
        if len(posList2) != 4:
            cv.circle(resized2, (x, y), 5, colors[len(posList2)], -1)
            posList2.append((x, y))
            print(posList2)
            cv.imshow("whiteboard 2", resized2)
            posNp2 = np.float32(posList2)  # convert to numpy for other usages
        else:
            return


while True:
    cv.setMouseCallback('whiteboard 1', draw_circle1)
    cv.setMouseCallback('whiteboard 2', draw_circle2)
    key = cv.waitKey(0)
    if key == ord('p'):
        alpha = 0.5
        beta = (1.0 - alpha)
        val = width/2-50

        # dist = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  # points ser to corner
        dist = np.float32([[val, val], [width-val, val], [val, height-val], [width-val, height-val]])  # points ser to corner
        new_matrix1 = cv.getPerspectiveTransform(posNp1, dist)
        new_matrix2 = cv.getPerspectiveTransform(posNp2, dist)
        result1 = cv.warpPerspective(resized, new_matrix1, (width, height))
        cv.imshow("result1", result1)
        result2 = cv.warpPerspective(resized2, new_matrix2, (width, height))
        cv.imshow("result2", result2)

        final = cv.addWeighted(result1, alpha, result2, beta, 0.0)
        cv.namedWindow('final', cv.WINDOW_AUTOSIZE)
        cv.imshow('final', final)
    if key == 27:
        break
cv.destroyAllWindows()
