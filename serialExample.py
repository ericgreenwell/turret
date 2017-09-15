#!usr/bin/bash python

from time import sleep
import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial_EIGHTBITS, timeout =0)

ser.write(':V#')
print ser.read()

ser.write(':MountInfo#')
print ser.read()

ser.close()
