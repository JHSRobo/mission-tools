# import the necessary packages

s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
import cv2
import numpy as np
class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		global s1
		global s2
		global s3
		global s4
		global s5
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# if the shape is a triangle, it will have 3 vertices
		##if len(approx) == 2:
		##	shape = "line"
		##	s1 = s1 + 1
		if len(approx) == 3:
			shape = "triangle"
			s2 = s2 + 1

		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			if ar >= 0.75 and ar <= 1.35:
				shape = "square"
				s3 = s3 + 1
			else:
				shape = "rectangle"
				s4 = s4 + 1

		# if the shape is a pentagon, it will have 5 vertices
		##elif len(approx) == 5:
			##shape = "pentagon"

		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
			s5 = s5 + 1

		# return the name of the shape
		print(s1,"lines,", s2, "triangles,", s3, "Squares,", s4, "rectangles,", s5, "circles")
		c1 = str(s1)
		c2 = str(s2)
		c3 = str(s3)
		c4 = str(s4)
		c5 = str(s5)
		blackdrop = np.zeros((1024,512,3), np.uint8)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(blackdrop,c2,(10,120), font, 4,(255,255,255),2,cv2.LINE_AA)
		cv2.putText(blackdrop,c3,(10,230), font, 4,(255,255,255),2,cv2.LINE_AA)
		cv2.rectangle(blackdrop,(125,155),(195,225),(0,255,0),-1)
		cv2.putText(blackdrop,c4,(10,340), font, 4,(255,255,255),2,cv2.LINE_AA)
		cv2.rectangle(blackdrop,(155,265),(165,335),(255,255,0),-1)
		cv2.putText(blackdrop,c5,(10,450), font, 4,(255,255,255),2,cv2.LINE_AA)
		cv2.circle(blackdrop,(160,410), 40, (0,0,255), -1)
		cv2.imshow("blackdrop", blackdrop)
		return shape
