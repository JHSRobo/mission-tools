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
	cv2.imshow('frame', frame)
	gray=cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	#edged = cv2.Canny(frame, 10, 250)
	ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
	thresh = cv2.adaptiveThreshold(blurred ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,6)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	idx = 0
	for c in cnts:
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
		cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		x,y,w,h = cv2.boundingRect(c)
		if w>60 and h>60:
			idx+=1
			new_img=frame[y:y+h,x:x+w]
			cv2.imshow(str(idx) + '.png', new_img)
	cv2.imshow("im",thresh)
	k = cv2.waitKey(33)
	if k==97:
		mode = 1
		break
	elif k==115:
		mode = 2
		break
	elif k==255:
		continue
