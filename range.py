
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("num.jpg") # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'))
print(text)


#https://stackoverflow.com/questions/17672705/text-detection-on-seven-segment-display-via-tesseract-ocr
#https://stackoverflow.com/questions/30479002/digital-numbers-on-tesseract-ocr
>>>>>>> 8766916f54819ff80218142354b438b5d542e5d7
