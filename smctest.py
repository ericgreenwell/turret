#Import pysmc
from SMC import *
from time import sleep
#create object on ttyUSB0 from dmesg | grep tty
smc100 = SMC100(1, "/dev/newport", silent=False)
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
print "no errors"

smc100.move_absolute_mm(10)
time.sleep(1.5)
smc100.stop()
# Clean Up
del smc100
