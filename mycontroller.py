#!/usr/bin/env python

import pygame
import pygame.camera
import time
import RPi.GPIO as GPIO
import serial
from subprocess import Popen, PIPE
from time import sleep
import pygame.camera
from pygame.locals import *
import os
#import sevenSeg
#from sevenSeg import measure
from SMC import *
import sys
#from PIL import Image
#import pytesseract

# Disable video drivers incase failed closeout
os.system("sudo modprobe -r uvcvideo")
time.sleep(2)
os.system("sudo modprobe uvcvideo")

############### Config #######################
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

############## Initiate Pygame ################
pygame.init()
pygame.camera.init()
pygame.display.init()
pygame.font.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

modes = pygame.display.list_modes()

VID = '/dev/video0'
MOUNT = '/dev/ioptron'
NEWPORT = '/dev/newport'
FLARE = '/dev/flare'

display = pygame.display.set_mode(modes[0], FULLSCREEN)
screen = pygame.surface.Surface(modes[0], 0, display)
pygame.display.set_caption("Range Capture")
clock = pygame.time.Clock()

############## Open Hardware Connections #############
try:
	mount = serial.Serial(MOUNT, baudrate=9600,bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout =0)
	newport = SMC100(1, NEWPORT, silent=True) #10 ms for each  command
	#flare = serial.Serial(FLARE, baudrate=9600,bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,timeout=0.5)
	camera = pygame.camera.Camera(VID, modes[0])
except:
   	os.system("sudo modprobe -r uvcvideo")
	os.system("sudo modprobe uvcvideo")
	camera = pygame.camera.Camera(VID, modes[0])
	print "One or more devices are not plugged in"

# serial number and ID of Serial Device: persistant naming in /etc/udev/rules.d/99-usb-serial.rules
camera.start()
mount.write(':V#')
newport.reset_and_configure()
newport.home(waitStop=True)
print "Initializing hardware connection..."
mount.write(':SR9#') # set speed
print "Mount Speed Max"
mount.write(':MH#')   #move mount home preassigned zero position
print "Moving home"
time.sleep(5)

############################################################
# Set speed "SRn#" where n=1-9
# mimic arrow press ":m[n,e,s,w]#" 
# to stop this ":q#" or ":q[R,D]#" for 

########## GPIO SETUP #############3
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

############### Variable Definitions #####################
threshold = .5
global speed
speed = 9
global dist
dist = 0
global newportPosition
newportPosition = 0
standoff = 0

############### function definitions ###########
def rangeMeasure():
        pic = camera.get_image(screen)
	#truncate
	#pic=pic[0:10,0:10]
	#may need to save/open/and turn gray
	text = pytesseract.image_to_string(pic)
	#text = sevenSeg.measure(pic)

	print text
	standoff = text
	#cv2.imwrite("rangeMeasure.jpg", im[0:0, 0:0]) #y:y+h x:x+w from top left
	
def rangeFocus(standoff):
	dist = standoff
	#newport_position = somefunction
	#newport.move_absolute_mm(self,newport_position, waitStop=True)
	#flarePostion = somefunction based on tigonometry
	#flare.write("{}".format(flarePosition))
	#numsteps = 	
	print(">>> Adjusting for range of {} to target".format(standoff))
	# automate telescope here!
	
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 40)

    def printy(self, display, textString):
        textBitmap = self.font.render(textString, True, RED)
        display.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 50
        
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

    #textPrint(display, "Time: {}".format(datetime.now())
    textPrint.printy(display, "Newport Position: {} um".format(newportPosition))
    textPrint.printy(display, "Mount Speed (1-9): {}".format(speed))
    textPrint.printy(display, "Standoff: {} m".format(standoff))
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done == True
	    cam.stop()
	    pygame.quit()
            sys.exit()
	    os.system("sudo modprobe -r uvcvideo")
            os.system("sudo modprobe uvcvideo")

    LR = joystick.get_axis(2)        	# Right Joystick L/R
    quit = joystick.get_button(12)    	# PS Button
    UD = joystick.get_axis(5)		# Right Joystick U/D
    DirPad = joystick.get_hat(0)	# Dpad
    range = joystick.get_button(3)	# X
    home  = joystick.get_button(1)    # Triangle
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
	print "Mount Speed: {}".format(speed)

    elif DirPad[1] == -1 and speed > 1:
	speed -= 1
	mount.write(":SR{}#".format(speed))
	print "Mount Speed: {}".format(speed)
	
	######### HOMING #######
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
	#rangeFocus(dist)
################## QUIT #########################
    
    elif quit:
	done = True
########## UPDATE AND DRAW #################3
    
    pygame.display.flip()	      
    clock.tick()	 
     
########### CLOSE AFTER QUIT ############
newport.close()
mount.close()
camera.stop()

#os.system("sudo modprobe -r uvcvideo")
#os.system("sudo modprobe uvcvideo")
############ EOF ###############

