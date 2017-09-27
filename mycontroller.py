import pygame
import time
import RPi.GPIO as GPIO
import serial
import subprocess
import picamera
import sevenSeg
from sevenSeg import measure
from smc100 import *


############## Open connection to Mount#############
mount = serial.Serial('/dev/ttyUSB0', baudrate=9600,bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout =0)
newport = smc100(1, '/dev/ttyUSB0', silent=False) #10 ms for each  command
camera = picamera.Picamera()



mount.write(':V#')
print "Initializing connection"
mount.write(':MountInfo#')
mount.write(':SR9#') # set speed
print "Mount Speed Max"
mount.write(':MH#')   #move mount home preassigned zero position
newport.home()
print "Moving home"
time.sleep(10)  
############################################################
# Set speed "SRn#" where n=1-9
# mimic arrow press ":m[n,e,s,w]#" 
# to stop this ":q#" or ":q[R,D]#" for 


########## GPIO SETUP #############3
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Label Pins
dirFlare = 25
stepFlare = 23
homeFlare = 21

#dirScope = 
#stepScope = 
#homeScope = 

one32 = 12  #pin for 1/32 of a step

#Setup Pins
GPIO.setup(dirFlare, GPIO.OUT)
GPIO.setup(stepFlare, GPIO.OUT)
GPIO.setup(homeFlare, GPIO.IN)
#fine motion
GPIO.setup(one32, GPIO.OUT)
#################################################
#settings for motors

threshold = .35
global speed
speed = 9
global dist
dist = 0

############# initialize Pygame ###############
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


############### function definitions ###########
def range():
	camera.capture('rangeMeasure.jpg')
	sevenSeg.measure()
	return dist
	
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
	print(">>> Adjusting for range of {} to target".format(range))
	# automate telescope here!

def Flare(flare):
	if flare > 0:
		GPIO.output(dirFlare, True)
	else:
		GPIO.output(dirFlare, False)
		
	GPIO.output(stepFlare, True)
	GPIO.output(stepFlare, False)
	

done = False
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

while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done == True
    LR = joystick.get_axis(2)        	# Right Joystick L/R
    home = joystick.get_button(0)    	# Square
    UD = joystick.get_axis(5)		# Right Joystick U/D
    DirPad = joystick.get_hat(0)	# Dpad
    range = joystick.get_button(3)	# X
    #button = joystick.get_button(1)    # Triangle
    track = joystick.get_button(2)	# Circle
    LLR = joystick.get_axis(0)		# Left Joystick L/R
    flare = joystick.get_axis(1)	# Left Joystick U/D
    zoomIN = joystick.get_button(4)	# Right Bumper
    zoomOUT = joystick.get_button(5)	# Left Bumper

######## Button Map #########################
"""
Axes = 6
0 Left Joystick LR
1 Left Joystick UD
2 Right Joystick LR
3 Left Trigger
4 Right Trigger
5 Right Joystick UD

Buttons: 14
0:Square 
1 X
2 Circle
3 Triangle
4 Left Bumper
5 Right Bumper
6 Left Trigger 
7 Right Trigger 
8 Share
9 Options
10 Left Joystick Press
11 Right Joystick Press
12 PS Button
13 Center Large Button

Hats: 1
 D-pad
 (0,0)
(L/R, U/D)
 Left Minus Down Minus
 Right Pos  Up Pos
"""
    ########## Conditions #############

	##### Motion #######

    if LR < -threshold and not flagLeft:
        mount.write(":mn#")
	flagLeft = True
	flagStopPan = False
	print "lefting"

    elif LR > threshold and not flagRight:
        mount.write(":ms#")
        flagRight = True
	flagStopPan = False
	print "Righting"
	
    elif UD > threshold and not flagUp:
	mount.write(":me#")
	flagUp = True
	flagStopTilt = False
	print "upping"
	
    elif UD < -threshold and not flagDown:
	mount.write(":mw#")
	flagDown = True
	flagStopTilt = False
	print "downing"

    elif LR > -threshold and LR < threshold and not flagStopPan:
        mount.write(":qD#")
	flagLeft = False
	flagRight= False
	flagStopPan = True
	print "stop lefting"
	
    elif UD > - threshold and UD < threshold and not flagStopTilt:
	mount.write(":qR#")
	print "stop upping"
	flagUp = False
	flagDown = False
	flagStopTilt = True

    elif track:
	subprocess.call('python', '~/CMT/run.py')
	

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
	print "homing"
	time.sleep(10)
        flagLeft = False
	flagRight = False
	flagUp = False
	flagDown = False

    elif range:
	#access measure function this may change based on range finder
	measure()
	rangeFocus(dist)

    elif zoomIn():
	#smc.move_relative_um(100)
	# use ser.write("1PT.1")
	#time.sleep(1)
	GPIO.output(dirScope, True)
	GPIO.output(stepScope, True)
	GPIO.output(stepScope, False)
	
    elif zoomOut():
	#smc.move_relative_um(-100)
	GPIO.output(dirScope, False)
	GPIO.output(stepScope, True)
	GPIO.output(stepScope, False)

    time.sleep(.1)    
############EOF###############
