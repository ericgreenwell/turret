#!/usr/bin/env python

import pygame
import pygame.camera
import time
import RPi.GPIO as GPIO
import serial
from subprocess import Popen, PIPE
import time
from datetime import datetime
import pygame.camera
from pygame.locals import *

#import sevenSeg
#from sevenSeg import measure
from SMC import *
import sys
#from PIL import Image
#import pytesseract

############### Config #######################
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)


############## Initiate Pygame ################
pygame.init()
pygame.camera.init()
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((800,480))
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'

display = pygame.display.set_mode(SIZE,0)
camera = pygame.camera.Camera(DEVICE, SIZE)
camera.start()
screen = pygame.surface.Surface((640,480), 0, display)
pygame.display.set_caption("Range Capture")
clock = pygame.time.Clock()

"""
def texts(dist):
    font = pygame.font.Font(None, 30)
    text=font.render("Newport Position:{}".format(newportPosition),1,(255,255,255))
    screen.blit(text, (0,0))
"""

############## Open connection to Mount#############
try:
	mount = serial.Serial('/dev/ioptron', baudrate=9600,bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout =0)
	newport = SMC100(1, '/dev/newport', silent=True) #10 ms for each  command
except:
   	print "One or more devices are not plugged in"

# serial number and ID of Serial Device: persistant naming in /etc/udev/rules.d/99-usb-serial.rules

mount.write(':V#')
newport.reset_and_configure()
newport.home()
print "Initializing hardware connection..."
mount.write(':MountInfo#')
print "Mount Info: {}".format(mount.readline())
mount.write(':SR9#') # set speed
print "Mount Speed Max"
mount.write(':MH#')   #move mount home preassigned zero position
print "Moving home"
  
############################################################
# Set speed "SRn#" where n=1-9
# mimic arrow press ":m[n,e,s,w]#" 
# to stop this ":q#" or ":q[R,D]#" for 

########## GPIO SETUP #############3
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#################################################
#settings for motors
threshold = .35
global speed
speed = 9
global dist
dist = 0
global newportPosition
newporPosition = 0
standoff = 0

############### function definitions ###########
def range():
        cam = cv2.VideoCapture(1)
	s, im = cam.read()
	#may need to save/open/and turn gray
	text = pytesseract.image_to_string(Image.open(im))
	print text
	return text
	cv2.imwrite("rangeMeasure.jpg", im[0:0, 0:0]) #y:y+h x:x+w from top left

#	camera.capture('rangeMeasure.jpg')
#	sevenSeg.measure()
#	return dist
	
def rangeFocus(dist):
	dist=dist
	#newport_position = somefunction
	#newport.move_absolute_mm(self,newport_position, waitStop=True)
	#flarePostion = somefunction based on tigonometry
	#numsteps = 	
	for i in range(numsteps):
		GPIO.output(flare, True)
		GPIO.output(flare, False)
		time.sleep(.001)
	print(">>> Adjusting for range of {} to target".format(dist))
	# automate telescope here!
"""
def flare(flare):
	if flare > 0:
		GPIO.output(dirFlare, True)
	else:
		GPIO.output(dirFlare, False)
		
	GPIO.output(stepFlare, True)
	GPIO.output(stepFlare, False)
"""	
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printy(self, display, textString):
        textBitmap = self.font.render(textString, True, RED)
        display.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
	

done = False
textPrint = TextPrint()  #create instance of print text

############### handler ##################       
#if name = "__main__":
flagLeft = False
flagRight = False
flagUp = False
flagDown = False
flagStopPan = False
flagStopTilt = False
flagSpeed = False
flagSpeedUp = False
flagSpeedDown = False
newportStopped = True

while done==False:
    screen.fill(WHITE)
    display.fill(WHITE)
    textPrint.reset()
    screen = camera.get_image(screen)
    display.blit(screen, (0,0))

    textPrint(display, "Time: {}".format(datetime.now())
    textPrint(display, "Newport Position: {}".format(newportPosition))
    textPrint(display, "Standoff: {}.format(standoff))
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done == True
	    cam.stop()
	    pygame.quit()
            sys.exit()

    LR = joystick.get_axis(2)        	# Right Joystick L/R
    home = joystick.get_button(12)    	# PS Button
    UD = joystick.get_axis(5)		# Right Joystick U/D
    DirPad = joystick.get_hat(0)	# Dpad
    range = joystick.get_button(3)	# X
    #button = joystick.get_button(1)    # Triangle
    track = joystick.get_button(2)	# Circle
    LLR = joystick.get_axis(0)		# Left Joystick L/R
    flare = joystick.get_axis(1)	# Left Joystick U/D
    rightBumper = joystick.get_button(4)	# Right Bumper
    leftBumper = joystick.get_button(5)	# Left Bumper

######## Button Map #########################

    ########## Conditions #############

	###### Mount Motion #######

    if LR < -threshold and not flagLeft:
        mount.write(":mn#")
	flagLeft = True
	flagStopPan = False

    elif LR > threshold and not flagRight:
        mount.write(":ms#")
        flagRight = True
	flagStopPan = False
		
    elif UD > threshold and not flagUp:
	mount.write(":mw#")
	flagUp = True
	flagStopTilt = False
		
    elif UD < -threshold and not flagDown:
	mount.write(":me#")
	flagDown = True
	flagStopTilt = False
	
    elif LR > -threshold and LR < threshold and not flagStopPan:
        mount.write(":qD#")
	flagLeft = False
	flagRight= False
	flagStopPan = True
		
    elif UD > - threshold and UD < threshold and not flagStopTilt:
	mount.write(":qR#")
	flagUp = False
	flagDown = False
	flagStopTilt = True

	######## Speed ########
    elif DirPad[1] == 1 and speed < 9:
	speed += 1
	mount.write(":SR{}#".format(speed))
	print "speed uping"
	print speed

    elif DirPad[1] == -1 and speed > 1:
	speed -= 1
	mount.write(":SR{}#".format(speed))
	print "speed downing"
	print speed
	
    elif home:
        mount.write(":MH#")
	newport.home()
        flagLeft = False
	flagRight = False
	flagUp = False
	flagDown = False
	
############# Beam Expander Motion ##################
	
    elif rightBumper < threshold and leftBumper < threshold and newportStopped== False:
	newport.sendcmd('ST')
	newportStopped = True
	newportPosition = newport.get_position_um()
	return newportPosition
	
    elif rightBumper > threshold and newportStopped == True:
	newport.move_absolute_mm(25)
	newportStopped = False
	
    elif leftBumper > threshold and newportStopped == True:
	newport.move_absolute_mm(0)
	newportStopped = False

############### Track and Range #####################

    elif range:
	#access measure function this may change based on range finder
	measure()
	rangeFocus(dist)
    """
    elif track:
	subprocess.call('python', 'run.py', shell=True)
    """	
    
    #texts(newportPosition)
    time.sleep(.1)    
    pygame.display.flip()
	      
    clock.tick()	      
########### CLOSE ############
newport.close()
mount.close()
############ EOF ###############

