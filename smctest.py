#Import pysmc
from smc100 import *
from time import sleep
#create object on ttyUSB0 from dmesg | grep tty
smc100 = SMC100(1, "/dev/ttyUSB0", silent=False)
print "resetting"
smc100.reset_and_configure()
sleep(5)

print "getting position"
print smc100.get_position_mm()

sleep(5)
print "moving home"
smc100.home()
sleep(10)
#make sure there are no errors

assert smc100.get_status()[0] == 0

pos = smc100.get_position_mm()
print "moving 5mm absolute"
smc100.move_absolute_mm(5)
sleep(5)
print "moving 3 relative"
smc100.move_relative_mm(3)

assert smc100.get_status()[0] ==0

# Clean Up
del smc100
