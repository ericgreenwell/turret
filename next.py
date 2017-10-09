#!/usr/bin/env python

import pygame
import time
from datetime import datetime
import pygame.camera
from pygame.locals import *
import cv2

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
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
    

pygame.init()
pygame.camera.init()
 
# Set the width and height of the screen [width,height]
#size = [800, 480]
#screen = pygame.display.set_mode(size)
display = pygame.display.set_mode(SIZE,0)
camera = pygame.camera.Camera(DEVICE, SIZE)
camera.start()
screen = pygame.surface.Surface((640,480), 0, display)


pygame.display.set_caption("Range Capture")
#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()    
# Get ready to print
textPrint = TextPrint()
count = 0
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    display.fill(WHITE)
    textPrint.reset()
    screen = camera.get_image(screen)
    #cv2.putText(screen, "time:{}".format(datetime.now()), (0,0), cv2.FONT_HERSHEY_SIMPLEX,2,255)
    display.blit(screen, (0,0))	
    
	# Get count of joysticks
    #joystick_count = pygame.joystick.get_count()

    textPrint.printy(display, "Time: {}".format(datetime.now()))
    textPrint.printy(display, "Count:{}".format(count))

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    count += 1
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
camera.stop()
