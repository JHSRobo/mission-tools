import cv2
import numpy as np

image = cv2.imread('benthiccrop.jpg')
_,contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]
## Convert to YUV color space to seperate luminosity
image_yuv = cv2.cvtColor(image,cv2.COLOR_BGR2YUV)
image_y = np.zeros(image_yuv.shape[0:2],np.uint8)
image_y[:,:] = image_yuv[:,:,0]
## Blur image to reduce high frequency noises from shapes
image_blurred = cv2.GaussianBlur(image_y,(3,3),0)

## Canny edge detector
edges = cv2.Canny(image_blurred,100,300,apertureSize = 3)

## FInd contours
contours,hierarchy, _ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

## For each contour, find the convex hull
hull = cv2.convexHull(cnt)
simplified_cnt = cv2.approxPolyDP(hull,0.001*cv2.arcLength(hull,True),True)

## Transfrom the quadrilateral into a rectangle
(H,mask) = cv2.findHomography(cnt.astype('single'),np.array([[[0., 0.]],[[2150., 0.]],[[2150., 2800.]],[[0.,2800.]]],dtype=np.single))

##
final_image = cv2.warpPerspective(image,H,(1000, 1000))

cv2.imshow("Show",final_image)
cv2.imwrite("img5_rect.png", final_image)
cv2.waitKey(0)
