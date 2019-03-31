#!/usr/bin/env/
# USAGE
#needs ros support but no one wants to do it.


# import the necessary packages
#from edgedetect.shapedetector import ShapeDetector
from edgedetect.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np
import os
import sys
cap = cv2.VideoCapture(0)
while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	resized = imutils.resize(frame, width=640)
	ratio = frame.shape[0] / float(resized.shape[0])
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
	lower_red = np.array([103,120,50])
	upper_red = np.array([130,255,255])
	k = cv2.waitKey(33)
	if k==97:
		#if you dare to touch the A key it will stop the program if it doesnt stop automatically
		break
	elif k==255:
		continue
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	#thresh = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
		cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
		shape = sd.detect(c)
		if shape == "square":
			print("crack")
		if shape == "rectangle":
			cv2.imwrite("is-it-a-rectange.png", mask)
			sqtest = cv2.imread("is-it-a-rectange.png", 0)
			y = 110
			x = 120
			h = 285
			w = 380
			crop = sqtest[y:y+h, x:x+w]
			thresh = cv2.adaptiveThreshold(crop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]
			sd = ShapeDetector()
			for c in cnts:
				# compute the center of the contour, then detect the name of the
				# shape using only the contour
				M = cv2.moments(c)
				cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
				cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
				shape = sd.detect(c)
				if shape == "square":
					print("crack")
				if shape == "rectangle":
					c = c.astype("float")
					c *= ratio
					c = c.astype("int")
					cv2.drawContours(thresh, [c], -1, (0, 255, 0), 2)
					cv2.putText(thresh, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
					cv2.imshow('thresh',thresh)
					cv2.imwrite("foundthecrack.png", frame)
					sys.exit("found the crack!")
					k = 97
					break
				else:
					try:
						os.remove("my.png")
					except: pass

				# multiply the contour (x, y)-coordinates by the resize ratio,
				# then draw the contours and the name of the shape on the image
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
				cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
	#thresh = cv2.adaptiveThreshold(hsv ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,6)
	#ret, thresh2 = cv2.threshold(ret, 60, 255, cv2.THRESH_BINARY_INV)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	#cv2.imshow('thresh',thresh)
	#cv2.imshow('thresh2',thresh2)
