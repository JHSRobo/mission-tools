#!/usr/bin/env/
# USAGE

#This code was created by me, Adam Graham, and was inspired by the tutorial found here https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/

# import the necessary packages
from edgedetect.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np
s2 = s3 = s4 = s5 = 0

# IP address where the camera is. THIS IS FOR THE AXIS / WEBCAM ONLY. This should be updated in ROSBasic to work with ros
# in package shape_detect
# https://github.com/JHSRobo/ROSBasic
IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"
#IP_ADDRESS = 0
# load the image/video
cap = cv2.VideoCapture(IP_ADDRESS)
#cap = cv2.VideoCapture(0)

while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	cv2.imshow('frame', frame)
	k = cv2.waitKey(33)
	if k==97:
		mode = 1
		ret, frame = cap.read()
		break
	elif k==115:
		mode = 2
		ret, frame = cap.read()
		break
	elif k==255:
		continue
# crop image to fit frame and resize it for better processing!


# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
##generic thresholhing
if mode == 2:
	ret, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
##adaptive threshholding
if mode == 1:
	thresh = cv2.adaptiveThreshold(blurred ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,13,5)
#ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #cvls2.THRESH_BINARY_INV,11,6)
cv2.imshow("thresh", thresh)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
idx=0
# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / (M["m00"] + 1e-7))
	cY = int(M["m01"] / (M["m00"] + 1e-7))
	shape = sd.detect(c)
	x,y,w,h = cv2.boundingRect(c)
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("int")
	if shape != "":
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        	cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
	#converts ints to strings

	# show the output image
cv2.imshow("Image", frame)

cv2.waitKey(0)
