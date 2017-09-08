import pygame
import time
import RPi.GPIO as GPIO
import serial
import subprocess


############## Open connection to Mount#############
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600,bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout =0)

ser.write(':V#')
print "Initializing connection"
ser.write(':MountInfo#')
ser.write(':SR9#') # set speed
print "Mount Speed Max"
ser.write(':MH#')   #move mount home preassigned zero position
print "Moving home"
time.sleep(5)  
############################################################
# Set speed "SRn#" where n=1-9
# mimic arrow press ":m[n,e,s,w]#" 
# to stop this ":q#" or ":q[R,D]#" for 


########## GPIO SETUP #############3
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Label Pins
dir_1 = 25
step_1 = 23
home_1 = 21

one32 = 12  #pin for 1/32 of a step

#Setup Pins
GPIO.setup(dir_1, GPIO.OUT)
GPIO.setup(step_1, GPIO.OUT)
GPIO.setup(home_1, GPIO.IN)
#fine motion
GPIO.setup(one32, GPIO.OUT)
#################################################
#settings for motors
axisUpDown = 5
axisLeftRight = 2
interval = float(0.1)
wait1 = .0001    #wait time dictates the speed of the stepper motor
threshold = .15
############# initialize Pygame ###############
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


############### function definitions ###########
    

done = False
############### handler ##################       
#if name = "__main__":
flagLeft = False
flagRight = False
flagStop = False

while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done == True
    LR = joystick.get_axis(2)        
    home = joystick.get_button(0)
    UD = joystick.get_axis(5)
    #LLR = joystick.get_axis(0)
    #LUD = joystick.get_axis(1)
    #zoomIN = joystick.get_button(4)
    #zoomOUT = joystick.get_button(5)
    ########## FLAGS #############
   # print LR, home, UD

    if LR < -threshold and not flagLeft:
        ser.write(":mn#")
	flagLeft = True
	print "lefting"

    elif LR > threshold and not flagRight:
        ser.write(":ms#")
        flagRight = True
	print "Righting"

    elif LR > -threshold and LR < threshold and not flagStop:
        ser.write(":q#")
	flagLeft = False
	flagRight= False
	flagStop = True
	print "stopping"
	
##    elif home:
#        ser.write(":MH#")
#	print "homing"


    time.sleep(.1)    
############EOF###############
