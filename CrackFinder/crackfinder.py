#!/usr/bin/env/

import argparse
import imutils
import cv2
import numpy as np
import os
import sys
from math import sqrt

IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"
#IP_ADDRESS = 0
RATIO = 1.85

previous_values = np.zeros((100,))
cap = cv2.VideoCapture(IP_ADDRESS)

def dist_form(first, last):
	return sqrt((first[0] - last[0])**2 + (first[1] - last[1])**2)

while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	resized = imutils.resize(frame, width=640)
	ratio = frame.shape[0] / float(resized.shape[0])
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_red = np.array([100,100,90])
	upper_red = np.array([140,255,255])
	k = cv2.waitKey(33)
	if k==97:
		#if you dare to touch the A key it will stop the program if it doesnt stop automatically
		break
	elif k==255:
		continue
	mask = cv2.inRange(hsv, lower_red, upper_red)
	#cv2.imshow("mask", mask)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	for cnt in cnts:
		if cv2.contourArea(cnt) > 2000:
			rect = cv2.minAreaRect(cnt)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			#print(box)
			height = dist_form(box[0], box[1])
			length = dist_form(box[0], box[3])
			width = min(height, length)
			#print(width)
			length = max(height, length)
			#print(length)			
			cv2.drawContours(frame, [box],0,(0,255,255),2)
			ratio = RATIO / width
			#print(ratio)
			cm_length = length * ratio
			rounded = round(cm_length, 1)
			print(rounded)
			if rounded > 8 and rounded < 20:
				previous_values = np.roll(previous_values, 1)
				previous_values[0] = cm_length
				if previous_values[-1] != 0:
					median = np.median(previous_values)
					print(median)
					less_array = previous_values <= (median + 1)
					greater_array = previous_values >= (median - 1) 
					tf_array = []
					for value in range(len(less_array)):
						#print(value)
						if less_array[value] and greater_array[value]:
							tf_array.append(True)
						else:
							tf_array.append(False)
					total = 0
					count = 0
					for tf, value in zip(tf_array, previous_values):
						if tf:
							total += value
							count += 1
					average = total / count
					rounded = round(average, 1)
					stringified = str(rounded) +"cm"
					cv2.putText(frame, stringified, (box[1][0], box[1][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
					cv2.imshow('frame', frame)
					cv2.waitKey(0)
					cv2.waitKey(0)
					sys.exit(0)


	cv2.imshow('frame',frame)

