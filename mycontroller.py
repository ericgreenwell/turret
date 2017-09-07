import pygame
import time
import RPi.GPIO as GPIO
#import asyncio
import serial

# Open connection to Mount
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial_EIGHTBITS, timeout =0)

ser.write(':V#')
print ser.read()

ser.write(':MountInfo#')
print ser.read()
ser.write(':SR9#') # set speed

ser.write(':MH#')   #move mount home preassigned zero position
print ser.read()

# Set speed "SRn#" where n=1-9
# mimic arrow press ":m[n,e,s,w]#" 
# to stop this ":q#" or ":q[R,D]#" for up/dwn




#ser.close()



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#sudo ds4drv

# Label Pins
dir_1 = 25
step_1 = 23
home_1 = 21

one32 = 12  #pin for 1/32 of a step

#Setup Pins
GPIO.setup(dir_1, GPIO.OUT)
GPIO.setup(dir_2, GPIO.OUT)
GPIO.setup(step_1, GPIO.OUT)
GPIO.setup(step_2, GPIO.OUT)

GPIO.setup(home_1, GPIO.IN)
GPIO.setup(home_2, GPIO.IN)

#fine motion
GPIO.setup(one32, GPIO.OUT)

#settings for motors
axisUpDown = 5
axisLeftRight = 2
interval = float(0.1)
wait1 = .0001    #wait time dictates the speed of the stepper motor
wait2 = .0001

threshold = .15
############# initialize Pygame ###############
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


############### function definitions ###########
def panLEFT(LR, dir_1, step_1, wait1):
    ser.write(':ms#')
    ser.write(':qD#')
    """GPIO.output(dir_1, True)
    GPIO.output(step_1,True)
    GPIO.output(step_1,False)
    print("moving left", LR)
    #time.sleep(wait1)
    """
def panRIGHT(LR, dir_1, step_1, wait1):
    ser.write(':mn#')
    ser.write(':qD#')
    """GPIO.output(dir_1, False)
    GPIO.output(step_1,True)
    GPIO.output(step_1,False)
    print("moving right", LR) 
    #time.sleep(wait1)
"""
def tiltUP(UD, dir_2, step_2, wait2):
    GPIO.output(dir_2, True)
    GPIO.output(step_2,True)
    GPIO.output(step_2,False)
    print("moving up", UD)
    #time.sleep(wait2)
    
def tiltDOWN(UD, dir_2, step_2, wait2):
    GPIO.output(dir_2, False)
    GPIO.output(step_2,True)
    GPIO.output(step_2,False)
    print("moving Down", UD)
    #time.sleep(wait2)

"""
#start fine controls
def panLEFTfine(LLR, dir_1, step_1, wait1, one32):
    GPIO.output(one32,True)
    GPIO.output(dir_1, True)
    
    GPIO.output(step_1,True)
    GPIO.output(step_1,False)
    print("fine left", LR)
    #time.sleep(wait1)
    GPIO.output(one32,False)
    
def panRIGHTfine(LLR, dir_1, step_1, wait1, one32):
    GPIO.output(one32,True)
    GPIO.output(dir_1, False)
    
    GPIO.output(step_1,True)
    GPIO.output(step_1,False)
    print("fine right", LR) 
    #time.sleep(wait1)
    GPIO.output(one32,False)
def tiltUPfine(LUD, dir_2, step_2, wait2, one32):
    GPIO.output(one32,True)
    GPIO.output(dir_2, True)
    
    GPIO.output(step_2,True)
    GPIO.output(step_2,False)
    print("fine up", UD)
    #time.sleep(wait2)
    GPIO.output(one32,False)
    
def tiltDOWNfine(LUD, dir_2, step_2, wait2, one32):
    GPIO.output(one32,True)
    GPIO.output(dir_2, False)
    
    GPIO.output(step_2,True)
    GPIO.output(step_2,False)
    print("fine Down", UD)
    #time.sleep(wait2)
    GPIO.output(one32,False)
#end fine contols
"""

def zoomIN():
    GPIO.output(one32, True)
    pass
def zoomOUT():
    pass

def home():
    print("going home")
    ser.write(':MH#')
    

done = False
############### handler ##################       
while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done == True
             
    LR = joystick.get_axis(2)        
    home = joystick.get_button(0)
    UD = joystick.get_axis(5)
    LLR = joystick.get_axis(0)
    LUD = joystick.get_axis(1)
    zoomIN = joystick.get_button(4)
    zoomOUT = joystick.get_button(5)

    if LR < -threshold:
        panLEFT(LR, dir_1, step_1, wait1)
        
    elif LR > threshold:
        panRIGHT(LR, dir_1, step_1, wait1)

    elif UD < -threshold:
        tiltUP(UD, dir_2, step_2, wait2)

    elif UD > threshold:
        tiltDOWN(UD, dir_2, step_2, wait2)

    elif LLR < -threshold:
        panLEFTfine(LLR, dir_1, step_1, wait1, one32)
        
    elif LLR > threshold:
        panRIGHTfine(LLR, dir_1, step_1, wait1, one32)

    elif zoomIN:
        #zoomIN()
        pass

    elif home:
        home()
    
   
    time.sleep(.0000001)
   
    
############EOF###############
