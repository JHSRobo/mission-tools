#!/usr/bin/env python
# USAGE
# needs ros support but no one wants to do it.

# import the necessary packages
import imutils
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from crack_finder.msg import crack_finder
from std_msgs.msg import Header
import cv2

class ShapeDetector:
	def __init__(self):
		self.s1 = self.s2 = self.s3 = self.s4 = self.s5 = 0
		pass

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		if len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			if 0.75 <= ar <= 1.35:
				shape = "square"
				self.s3 = self.s3 + 1
			else:
				shape = "rectangle"
				self.s4 = self.s4 + 1

		# return the name of the shape
		return shape

def find_the_shape():
	msg = crack_finder()

	header = Header()

	# update message headers
	header.stamp = rospy.Time.now()
	header.frame_id = 'humidity_data'
	msg.header = header

    try:
        data = rospy.wait_for_message("/rov/image_raw", Image, timeout=5)
    except rospy.ROSException:
        msg.length = None
		return msg
    else:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data.data, desired_encoding="passthrough")
        while True:
        	# Capture frame-by-frame
        	resized = imutils.resize(frame, width=640)
			ratio = frame.shape[0] / float(resized.shape[0])
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
			lower_red = np.array([103,140,50])
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
					#print("if 1.8: ", lengthsmallo)
					#print("if 1.9: ", lengthLARGO)
					j = "if 1.8: "
					i = str(lengthsmallo)
					m = j + i
					b = " if 1.9: "
					o = str(lengthLARGO)
					e = m + b + o
					msg.length = e
					return msg
	msg.length = None
	return msg


def listener():
    rospy.init_node("crack_finder")
    pub = rospy.Publisher("crack_finder", crack_finder, queue_size=2)
	rate = rospy.Rate(2)
	while not rospy.is_shutdown():
		pub.publish(find_the_shape())
		rate.sleep()



if __name__ == "__main__":
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
