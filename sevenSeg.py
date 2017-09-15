## import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np


def measure():
	# define the dictionary of digit segments so we can identify
	# each digit on the thermostat

	DIGITS_LOOKUP = {
		(1, 1, 1, 0, 1, 1, 1): 0,
		(0, 0, 1, 0, 0, 1, 0): 1,
		(1, 0, 1, 1, 1, 1, 0): 2,
		(1, 0, 1, 1, 0, 1, 1): 3,
		(0, 1, 1, 1, 0, 1, 0): 4,
		(1, 1, 0, 1, 0, 1, 1): 5,
		(1, 1, 0, 1, 1, 1, 1): 6,
		(1, 0, 1, 0, 0, 1, 0): 7,
		(1, 1, 1, 1, 1, 1, 1): 8,
		(1, 1, 1, 1, 0, 1, 1): 9
	}

	image = cv2.imread("rangeMeasure.jpg")
	# crop THIS IS SPECIFIC TO THIS IMAGE!!!
	image = image[2300:2700, 1400:1800]  #y:y+h x:x+w
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5), np.uint8)
	gray = cv2.dilate(gray, kernel, iterations=2)
	gray = cv2.erode(gray, kernel, iterations=2)


	thresh = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

	# find contours in the thresholded image, then initialize the
	# digit contours lists
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	digitCnts = []

	# loop over the digit area candidates
	for c in cnts:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(c)

		# if the contour is sufficiently large, it must be a digit
		if w >= 20 and (h >= 40 and h <= 250): #this eliminates "." and anomolies
			digitCnts.append(c)

	#cv2.imshow("image", thresh)
	#cv2.waitKey(0)
	# sort the contours from left-to-right, then initialize the
	# actual digits themselves
	digitCnts = contours.sort_contours(digitCnts,
		method="left-to-right")[0]
	digits = []

	# loop over each of the digits
	for c in digitCnts:
		# extract the digit ROI
		(x, y, w, h) = cv2.boundingRect(c)
		if w <= 40:		#account for "1" being small
			x = x-60
			w = 80
		
		roi = thresh[y:y + h, x:x + w]
		#cv2.imshow("roi", roi)
		#cv2.waitKey(0)
		# compute the width and height of each of the 7 segments
		# we are going to examine
		(roiH, roiW) = roi.shape
		(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
		dHC = int(roiH * 0.05)

		# define the set of 7 segments
		segments = [
			((0, 0), (w, dH)),	# top
			((0, 0), (dW, h // 2)),	# top-left
			((w - dW, 0), (w, h // 2)),	# top-right
			((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
			((0, h // 2), (dW, h)),	# bottom-left
			((w - dW, h // 2), (w, h)),	# bottom-right
			((0, h - dH), (w, h))	# bottom
		]
		on = [0] * len(segments)


		# loop over the segments
		for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
			# extract the segment ROI, count the total number of
			# thresholded pixels in the segment, and then compute
			# the area of the segment
			segROI = roi[yA:yB, xA:xB]
			total = cv2.countNonZero(segROI)
			area = (xB - xA) * (yB - yA)

			# if the total number of non-zero pixels is greater than
			# 50% of the area, mark the segment as "on"
			if total / float(area) > 0.5:
				on[i]= 1

		# lookup the digit and draw it on the image
		digit = DIGITS_LOOKUP[tuple(on)]
		digits.append(digit)
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
		cv2.putText(image, str(digit), (x - 10, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)


	# display the digits
	dist = "".join([str(digits[x]) for x in range(0, len(digits) - 1)]) + "." + str(digits[-1])
	print("Range: {}".format(dist))
	return dist
#	print(u"{}{}.{} m".format(*digits))
	cv2.imshow("Output", image)
	cv2.waitKey(0)
