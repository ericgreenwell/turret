
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy
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



# loop over training data and extract digits
for (i,c) in enumerate(refCnts):
	#compute bounding box
	(x,y,w,h) = cv2.boundingRect(c)
	roi = ref[y:w+h, x:x+w]
	roi = cv2.resize(roi, (57,88))

	#update digits dictionary
	digits[i] = roi


######## load image ###############33

image = cv2.imread("num.jpg")
image = imutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#find contours 
cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
locs = []

# loop over contours

for (i,c) in enumerate(cnts):
	(x,y,w,h) = cv2.boundingRect(c)
	ar = w/float(h)
	locs.append((x,y,w,h))

locs = sorted(locs, key=lambda x:x[0])
output = []

digitCnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
digitCnts = digitCnts[0]
digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

#####loop again###

for c in digitCnts:
	(x,y,w,h) = cv2.boundingRect(c)
	roi =gray[y:y+h, x:x+w]
	roi = cv2.resize(roi, (57,88)) 
	
	scores = []

	for (digit, digitROI) in digits.items():
		result = cv2.matchTemplate(roi, digitROI,cv2.TM_CCOEFF)
		(_, score, _, _) = cv2.minMaxLoc(result)
		scores.append(score)

print("range:{}".format(''.join(output)))
cv2.imshow("image", image)

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




def preprocessing(img):
	pass	

if __name__ == "__main__":
	getImage()


im = Image.open("num.jpg") # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'))
print(text)
"""

#https://stackoverflow.com/questions/17672705/text-detection-on-seven-segment-display-via-tesseract-ocr
#https://stackoverflow.com/questions/30479002/digital-numbers-on-tesseract-ocr

