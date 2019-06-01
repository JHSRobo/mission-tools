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
import rospy
from sensor_msgs.msg import Image
import os
import sys
from cv_bridge import CvBridge, CvBridgeError

IP_ADDRESS = "rtsp://root:jhsrobo@192.168.1.201/axis-media/media.amp"
def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
                       pts[1][0]:pts[2][0]]

    return img_crop

def callback(data):
    bridge = CvBridge()
    try:
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    resized = imutils.resize(frame, width=640)
    ratio = frame.shape[0] / float(resized.shape[0])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    lower_red = np.array([100,110,50])
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
        print(shape)
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
            #rotcrop = crop_minAreaRect(frame, rect)
            #cv2.imshow('croppo2', rotcrop)

        if shape == "rectangle":
            cv2.imwrite("is-it-a-rectange.png", mask)
            sqtest = cv2.imread("is-it-a-rectange.png", 0)
            y = 75
            x = 75
            h = 350
            w = 500
            crop = sqtest[y:y+h, x:x+w]
            thresh = cv2.adaptiveThreshold(crop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,13,2)
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
                    #quickmaffsSMALLO = bluesmallside / 1.85 (IDEAL LEN)
                    quickmaffsLARGO = bluesmallside / 1.85
                    #lengthsmallo = bluephatsize / quickmaffsSMALLO
                    lengthLARGO = bluephatsize / quickmaffsLARGO
                    if lengthLARGO  > 7.5:
                        #print(lengthLARGO)
                        rounded = round(lengthLARGO, 2)
                        stringified = str(rounded)
                        cv2.putText(frame, stringified, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
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

def listener():
    rospy.init_node('crack_detection')
    rospy.Subscriber("/rov/image_raw", Image, callback)
    rospy.spin()
if __name__ == '__main__':
    listener()
