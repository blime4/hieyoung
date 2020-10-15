import numpy as np
import argparse
import cv2



def four_point_transform(image, pts):

    # 获取坐标点，并将它们分离开来
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # 计算新图片的宽度值，选取水平差值的最大值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # 计算新图片的高度值，选取垂直差值的最大值
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # 构建新图片的4个坐标点
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
    # 获取仿射变换矩阵并应用它
    M = cv2.getPerspectiveTransform(rect, dst)
    # 进行仿射变换
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # 返回变换后的结果
    return warped



if __name__ == '__main__':

    image = cv2.imread("2.jpg")

    canny = cv2.Canny(image,50,150,3)

    cv2.imshow("1",canny)

    #寻找轮廓

    contours, hier = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxarea=0

    maxint=0

    i = 0

    for c in contours:

        if cv2.contourArea(c) > maxarea:

            maxarea=cv2.contourArea(c)

            maxint = i

            i +=1

    box = cv2.approxPolyDP(contours[maxint], 15, True) #多边形拟合 True 代表封闭

    print(box.shape)

    poly = np.zeros(canny.shape)

    cv2.polylines(poly, [box],True, (255, 0, 0)) #连线
    cv2.imshow("2",poly)
    cv2.waitKey()

    # 对原始图片进行变换

    # pts = np.array([(x,y),(x+w,y),(x+w,y+h),(x,y+h)], dtype = "float32")

    warped = four_point_transform(image, box)



    # 结果显示

    cv2.imshow("Original", image)

    cv2.imshow("Warped", warped)

    cv2.waitKey(0)