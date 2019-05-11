#!/usr/bin/env/
# USAGE
#needs ros support but no one wants to do it.


# import the necessary packages
#from edgedetect.shapedetector import ShapeDetector
from edgedetectforcrack.shapedetectorforcrack import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np
import os
import sys
#IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"
#cap = cv2.VideoCapture(IP_ADDRESS)
cap = cv2.VideoCapture(0)
while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	resized = imutils.resize(frame, width=640)
	ratio = frame.shape[0] / float(resized.shape[0])
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
	lower_red = np.array([100,120,50])
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
	idx = 0
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
		cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
		shape = sd.detect(c)
		x,y,w,h = cv2.boundingRect(c)
		if w>1 and h>1:
			idx+=1
			new_img = frame[y:y+h,x:x+w]
			cv2.imshow('croppo',new_img)
			cv2.imwrite('croppo.png', new_img)
			M = cv2.moments(c)
			cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
			cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			cv2.drawContours(frame, [c], -1, (0, 0, 255), 2)
			blueval0 = np.size(new_img, 0)
			blueval1 = np.size(new_img, 1)
			bluesmallside = min(blueval0, blueval1)
			bluephatsize = max(blueval0, blueval1)
			quickmaffsSMALLO = bluesmallside / 1.75
			quickmaffsLARGO = bluesmallside / 1.87
			lengthsmallo = bluephatsize / quickmaffsSMALLO
			lengthLARGO = bluephatsize / quickmaffsLARGO
			print("if 1.8: ", lengthsmallo)
			print("if 1.9: ", lengthLARGO)
		if shape == "rectangle":
			cv2.imwrite("is-it-a-rectange.png", mask)
			sqtest = cv2.imread("is-it-a-rectange.png", 0)
			y = 55
			x = 60
			h = 485
			w = 480
			#crop = sqtest[y:y+h, x:x+w]
			thresh = cv2.adaptiveThreshold(sqtest,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,13,2)
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]
			#print(cnts)
			sd = ShapeDetector()
			for c in cnts:
				# compute the center of the contour, then detect the name of the
				# shape using only the contour
				M = cv2.moments(c)
				cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
				cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
				shape = sd.detect(c)
				if shape == "rectangle":
					c = c.astype("float")
					c *= ratio
					c = c.astype("int")
					cv2.imshow('thresh',thresh)
					cv2.imwrite("foundthecrack.png", frame)
					blueval0 = np.size(new_img, 0)
					blueval1 = np.size(new_img, 1)
					bluesmallside = min(blueval0, blueval1)
					bluephatsize = max(blueval0, blueval1)
					quickmaffsSMALLO = bluesmallside / 1.8
					quickmaffsLARGO = bluesmallside / 1.9
					lengthsmallo = bluephatsize / quickmaffsSMALLO
					lengthLARGO = bluephatsize / quickmaffsLARGO
					print("if 1.8: ", lengthsmallo)
					print("if 1.9: ", lengthLARGO)
					#cv2.imwrite("foundthecrack.png", frame)
					#image4 = frame

					#gray3=cv2.cvtColor(image4,cv2.COLOR_BGR2GRAY)
					#edged = cv2.Canny(image4, 170, 250)
					#hsv = cv2.cvtColor(image4, cv2.COLOR_BGR2HSV)
					#lower_black = np.array([0,0,0])
					#upper_black = np.array([132,88,60])
					#thresh100 = cv2.inRange(hsv, lower_black, upper_black)
					#cv2.imshow('hsv', hsv)
					#blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
					#thresh3 = cv2.threshold(blurred3, 100, 255, cv2.THRESH_BINARY)
					#thresh3 = cv2.adaptiveThreshold(blurred3 ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,15,8)
					#cnts = cv2.findContours(thresh100.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
					#cnts = cv2.findContours(thresh3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
					#cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
					#cnts = cnts[0] if imutils.is_cv2() else cnts[1]
					#cv2.imshow('blackcrop', thresh100)
					#cv2.imshow('blackcrop', thresh3)
					#cv2.imshow('blackcrop', edged)
					'''for c in cnts:
						x,y,w,h = cv2.boundingRect(c)
						if w>100 and h>100:
							new_img1=image4[y:y+h,x:x+w]
							cv2.imshow('blackcrop.png', new_img1)
							cv2.imwrite('blackcrop.png', new_img1)
							heightblk = np.size(new_img1, 0)
							widthblk = np.size(new_img1, 1)
							heightblu = np.size(new_img, 0)
							widthblu = np.size(new_img, 1)
							print("blkpixel height", heightblk)
							print("blkpixel width", widthblk)
							print("bluepixel width", widthblu)
							print("bluepixel height", heightblu)
							actualheightblk = 31.0/heightblk
							actualwidthblk = 31.0/widthblk
							actualheightblu = actualheightblk*heightblu
							actualwidthblu = actualwidthblk*widthblu
							print("actualheightblue", actualheightblu)
							print("actualwidthblue", actualwidthblu)
							M = cv2.moments(c)
							cX = int((M["m10"] / (M["m00"] + 1e-7)) * ratio)
							cY = int((M["m01"] / (M["m00"] + 1e-7)) * ratio)
							c = c.astype("float")
							c *= ratio
							c = c.astype("int")
							cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
							#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
							#sys.exit("found the crack!")
							k = 97
							break
						else:
							try:
								os.remove("foundthecrack.png")
							except: pass
'''
			# multiply the contour (x, y)-coordinates by the resigratio
			# then draw the contours and the name of the shape on the image
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			#cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
			#cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		#cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		#cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
	#thresh = cv2.adaptiveThreshold(hsv ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,6)
	#ret, thresh2 = cv2.threshold(ret, 60, 255, cv2.THRESH_BINARY_INV)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	#cv2.imshow('thresh',thresh)
	#cv2.imshow('thresh2',thresh2)
