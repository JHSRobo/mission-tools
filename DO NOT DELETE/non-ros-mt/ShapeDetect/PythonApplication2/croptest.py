import argparse
import imutils
import cv2
import numpy as np

frame = cv2.imread("video.jpg")
cv2.rectangle(frame, (50, 110), (330, 390), (255, 255, 255), 3)
cv2.imshow('frame', frame)
y = 110
x = 50
h = 280
w = 280
crop = frame[y:y+h, x:x+w]
cv2.imshow('crop', crop)
k = cv2.waitKey(0)
