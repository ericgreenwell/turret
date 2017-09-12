import picamera
import image
import tesseract
# sudo apt-get install tesseract-ocr

def capture():
	picamera.capture("range.jpg")
	
def measure():
	img = Image.open("/home/pi/control/range.jpg")
	cropped_img = img.crop() # img.crop(x1,y1,x2,y2) left and top start
	range = pytesseract.image_to_string(cropped, config= ' outputbase digits')
	print range
