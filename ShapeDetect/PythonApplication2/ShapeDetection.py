#!/usr/bin/env/
# USAGE
#needs ros support but no one wants to do it.


# import the necessary packages
from edgedetect.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np


# load the image/video
cap = cv2.VideoCapture(0)
while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	cv2.rectangle(frame, (110, 400), (510, 100), (255, 255, 255), 3)
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('p'):
		break
# crop image to fit frame and resize it for better processing!
y = 110
x = 120
h = 285
w = 380
crop = frame[y:y+h, x:x+w]
resized = imutils.resize(crop, width=520)
ratio = crop.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
##generic thresholhing
#ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
##adaptive threshholding
thresh = cv2.adaptiveThreshold(blurred ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,11,7)
#ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #cv2.THRESH_BINARY_INV,11,6)
cv2.imshow("thresh", thresh)
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
	cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
	shape = sd.detect(c)

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(crop, [c], -1, (0, 255, 0), 2)
	cv2.putText(crop, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
	# show the output image
cv2.imshow("Image", crop)

cv2.waitKey(0)
