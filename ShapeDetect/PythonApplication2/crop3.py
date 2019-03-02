import numpy as np
import cv2

image = cv2.imread('benthiccrop.jpg')
y=75
x=80
h=200
w=320
crop = image[y:y+h, x:x+w]
cv2.imshow('Image', crop)
cv2.waitKey(0)
