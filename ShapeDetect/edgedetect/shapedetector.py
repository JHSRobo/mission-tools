# import the necessary packages
import cv2
import numpy as np
from math import sqrt

def dist_form(first, last):
	# distance formula
	return sqrt((first[0] - last[0])**2 + (first[1] - last[1])**2)

class ShapeDetector:
	def __init__(self):
		self.s1 = self.s2 = self.s3 = self.s4 = self.s5 = 0
		pass

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = ""
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.035 * peri, True)
		#print(cv2.contourArea(approx))
		if not cv2.contourArea(approx) < 1500 and not cv2.contourArea(approx) > 10000:
			# if the shape is a triangle, it will have 3 vertices
			# if len(approx) == 2:
			# shape = "line"
			# s1 = s1 + 1
			if len(approx) == 3:
				shape = "triangle"
				self.s2 = self.s2 + 1

			# if the shape has 4 vertices, it is either a square or
			# a rectangle
			elif len(approx) == 4:
				# compute the bounding box of the contour and use the
				# bounding box to compute the aspect ratio
				(x, y, w, h) = cv2.boundingRect(approx)
				rect = cv2.minAreaRect(c)  # make a rectangle around it
				box = cv2.boxPoints(rect)
				box = np.int0(box)  # get the int coords
				height = dist_form(box[0], box[1])
				length = dist_form(box[0], box[3])
				if 0.5 < min(length, height) / max(length, height) < 1.5:
					shape = "square"
					self.s3 += 1
				elif 2.5 < max(length, height) / min(length, height) < 3.5:
					shape = "rectangle"
					self.s4 += 1

			else:
				(x,y), radius = cv2.minEnclosingCircle(approx)
				center = (int(x), int(y))
				#cv2.circle('thresh', center, int(radius), (0,255,255), 2)
				perfect_circle = cv2.ellipse2Poly(center, (int(radius), int(radius)), 0, 0, 360, 5)
				difference = cv2.matchShapes(approx, perfect_circle, 1, 0.0)
				#print(difference)
				if difference < 0.03:
					shape = "circle"
					self.s5 += 1


		c2 = str(self.s2)
		c3 = str(self.s3)
		c4 = str(self.s4)
		c5 = str(self.s5)
		blackdrop = np.zeros((512, 512, 3), np.uint8)
		font = cv2.FONT_HERSHEY_SIMPLEX
		#displays number of triangles
		cv2.putText(blackdrop,c2,(10,120), font, 4,(0,0,255),2,cv2.LINE_AA)
		#displays number of Squares
		cv2.putText(blackdrop,c3,(10,230), font, 4,(0,0,255),2,cv2.LINE_AA)
		p1 = (166, 40)
		p2 = (130, 120)
		p3 = (200, 120)
		# Drawing the triangle with the help of lines
		cv2.line(blackdrop, p1, p2, (0, 0, 255), 3)
		cv2.line(blackdrop, p2, p3, (0, 0, 255), 3)
		cv2.line(blackdrop, p1, p3, (0, 0, 255), 3)
		cv2.rectangle(blackdrop,(125,155),(195,225),(0,0,255),3)
		cv2.putText(blackdrop,c4,(10,340), font, 4,(0,0,255),2,cv2.LINE_AA)
		cv2.rectangle(blackdrop,(155,265),(165,335),(0,0,255),3)
		cv2.putText(blackdrop,c5,(10,450), font, 4,(0,0,255),2,cv2.LINE_AA)
		cv2.circle(blackdrop,(160,410), 40, (0,0,255), 3)
		cv2.imshow("blackdrop", blackdrop)
		return shape
