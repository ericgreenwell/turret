#import picamera
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import image_to_string
import time
import cv2
import os

# sudo apt-get install tesseract-ocr
# Python 3 file

def capture():
	picamera.capture("range.jpg")
	
def measure():
	
#	image = cv2.imread('/home/eric/turret/image.jpg')#
#	img.crop(x1,y1,x2,y2) left and top start

	im = Image.open("image.jpg")
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert("1")
	im.save("new.jpg")
	time.sleep(5)
	range = image_to_string(Image.open("image.jpg"))
	print(range)

if __name__ == "__main__":
	measure()
