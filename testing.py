import pytesseract
from pytesseract import image_to_string
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import imutils
from imutils import contours

print("OpenCV version: {}".format(cv2.__version__))

im = cv2.imread("rangeMeasure.jpg", 1) 
im = im[2300:2700, 1400:1800]

#cv2.imshow("image", im)
#cv2.waitKey(0)
#im = im.filter(ImageFilter.MedianFilter())
#enhancer = ImageEnhance.Contrast(im)
#im = enhancer.enhance(2)
#im = im.convert('1')
kernel = np.ones((7,7), np.uint8)
cv2.imwrite("test.jpg", im)
text= pytesseract.image_to_string(Image.open("test.jpg"))
print text
#for i in range(10):
#	im = cv2.dilate(im ,kernel, iterations = i)
#	cv2.imshow("dilation {}".format(i), im)
#	cv2.waitKey(0)
#	cv2.imwrite("test.jpg", im)
#	text = pytesseract.image_to_string(Image.open("test.jpg"))
#	print text
#im.save('temp2.jpg')
#text = pytesseract.image_to_string(Image.open('temp2.jpg'))
#print(text)

#https://stackoverflow.com/questions/17672705/text-detection-on-seven-segment-display-via-tesseract-ocr
#https://stackoverflow.com/questions/30479002/digital-numbers-on-tesseract-ocr

