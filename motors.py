import RPi.GPIO as GPIO
from time import sleep

pin = 23
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)


def tiltUP():
    print "going up!"
    GPIO.output(pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin, GPIO.LOW)
    sleep(1)
    GPIO.output(pin, GPIO.HIGH)

