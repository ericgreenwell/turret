import pytesseract
from pytesseract import image_to_string
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import imutils
from imutils import contours

print("OpenCV version: {}".format(cv2.__version__))

reference = "/home/eric/turret/new.jpg"
ref = cv2.imread(reference)
cv2.imshow("ref", ref)
cv2.waitKey(0)
ref = cv2.threshold(ref, 10, 225, cv2.THRESH_BINARY_INV)[1]
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}



#load image ###############33

image = cv2.imread("num.jpg")
image = imutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#find contours 
cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
locs = []
"""
def getImage():
	
	#take image and save in proper directory
	img = cv2.imread(path)
	cv2.imshow("image", img)
	cv2.waitKey(0)
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow("gray", img2)
	cv2.waitKey(0)
	img3 = cv2.GaussianBlur(img2, (7,7), 0)
	cv2.imshow("blur", img3)
	cv2.waitKey(0)

if __name__ == "__main__":
	getImage()
"""

im = Image.open("num.jpg") # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
kernel = np.ones((5,5), np.uint8)

for i in range(10):
	im = cv2.dilate(image,kernel, iterations = i)
	cv2.imshow("dilation {}".format(i), im)
	cv2.waitKey(0)
	cv2.imwrite("test.jpg", im)
	text = pytesseract.image_to_string(Image.open("test.jpg"))
	print text
#im.save('temp2.jpg')
#text = pytesseract.image_to_string(Image.open('temp2.jpg'))
#print(text)

#https://stackoverflow.com/questions/17672705/text-detection-on-seven-segment-display-via-tesseract-ocr
#https://stackoverflow.com/questions/30479002/digital-numbers-on-tesseract-ocr

