# 1.Aplicar una transformacion afin para invertir la imagen verticalmente
import cv2 as cv
import numpy as np

img = cv.imread("painting.jpg")
rows, cols, ch = img.shape

# we need three points to derive to affine transformation
# lets see the positions of the three points
cv.circle(img, (0, 0), 5, (0, 0, 255), -1)  # point on the top-left corner
cv.circle(img, (cols, 0), 5, (0, 255, 0), -1)  # point on the top-right corner
cv.circle(img, (0, rows), 5, (255, 0, 0), -1)  # point on the bottom-left corner

pts1 = np.float32([[0, 0], [cols, 0], [0, rows]])  # src points
pts2 = np.float32([[cols, rows], [0, rows], [cols, 0]])  # transf points, invert top-bottom

matrix = cv.getAffineTransform(pts1, pts2)  # get the affine transformation
result = cv.warpAffine(img, matrix, (cols, rows))  # apply the affine transformation to the image

cv.imshow("image", img)
cv.imshow("affine transformation", result)
cv.waitKey(0)
cv.destroyAllWindows()
