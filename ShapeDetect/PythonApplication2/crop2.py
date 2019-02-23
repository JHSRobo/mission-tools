import cv2
import numpy as np

image = cv2.imread('benthiccrop.png')
image_yuv = cv2.cvtColor(image,cv2.COLOR_BGR2YUV)
image_y = np.zeros(image_yuv.shape[0:2],np.uint8)
image_y[:,:] = image_yuv[:,:,0]
image_blurred = cv2.GaussianBlur(image_y,(3,3),0)
edges = cv2.Canny(image_blurred,100,300,apertureSize = 3)
contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
hull = cv2.convexHull(cnt)
simplified_cnt = cv2.approxPolyDP(hull,0.001*cv2.arcLength(hull,True),True)
(H,mask) = cv2.findHomography(cnt.astype('single'),np.array([[[0., 0.]],[[2150., 0.]],[[2150., 2800.]],[[0.,2800.]]],dtype=np.single))
final_image = cv2.warpPerspective(image,H,(2150, 2800))

cv2.imshow("Show",final_image)
cv2.imwrite("img5_rect.png", final_image)
cv2.waitKey(0)
