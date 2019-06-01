# import the necessary packages

s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
import cv2

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
		

		return shape
