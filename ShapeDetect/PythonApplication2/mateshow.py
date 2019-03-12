
def mateshow(x):
	if shape == x:
		s2 += 1
	if shape == x:
		s3 += 1
	if shape == x:
		s4 += 1
	if shape == x:
		circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
		if circles is not None:
			s5 += 1

	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(crop, [c], -1, (0, 255, 0), 2)
	cv2.putText(crop, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)
	#converts ints to strings
	c2 = str(s2)
	c3 = str(s3)
	c4 = str(s4)
	c5 = str(s5)
	#creates blackdrop for GUI
	blackdrop = np.zeros((512, 512, 3), np.uint8)
	font = cv2.FONT_HERSHEY_SIMPLEX
	#displays number of triangles
	cv2.putText(blackdrop,c2,(10,120), font, 4,(255,255,255),2,cv2.LINE_AA)
	#displays number of Squares
	cv2.putText(blackdrop,c3,(10,230), font, 4,(255,255,255),2,cv2.LINE_AA)
	p1 = (166, 40)
	p2 = (130, 120)
	p3 = (200, 120)
	# Drawing the triangle with the help of lines
	cv2.line(blackdrop, p1, p2, (255, 0, 0), 3)
	cv2.line(blackdrop, p2, p3, (255, 0, 0), 3)
	cv2.line(blackdrop, p1, p3, (255, 0, 0), 3)
	cv2.rectangle(blackdrop,(125,155),(195,225),(0,255,0),-1)
	cv2.putText(blackdrop,c4,(10,340), font, 4,(255,255,255),2,cv2.LINE_AA)
	cv2.rectangle(blackdrop,(155,265),(165,335),(255,255,0),-1)
	cv2.putText(blackdrop,c5,(10,450), font, 4,(255,255,255),2,cv2.LINE_AA)
	cv2.circle(blackdrop,(160,410), 40, (0,0,255), -1)
	cv2.imshow("blackdrop", blackdrop)
