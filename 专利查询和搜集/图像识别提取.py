import cv2
import numpy as np
import os

pngs = os.listdir("./png/")

image = cv2.imread("./png/4149339.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Image", gray)
# cv2.imwrite("contoursImage2.jpg", image)

# cv2.waitKey(0)
gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)


blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=50)


(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[1]
 
# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))
 
# draw a bounding box arounded the detected barcode and display the image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.imwrite("contoursImage2.jpg", image)

cv2.waitKey(0)


if not os.path.exists("png_cv2/"):
    os.mkdir("png_cv2")
