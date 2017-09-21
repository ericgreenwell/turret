#Import pysmc
from smc100 import *

#create object on ttyUSB0 from dmesg | grep tty
smc100 = SMC100(1, "/dev/ttyUSB0", silent=False)

print smc100.get_position_mm()

smc100.home()

#make sure there are no errors

assert smc100.get_status()[0] == 0

pos = smc100.get_position_mm()

smc.move_absolute_mm(5)
assert smc100.get_status()[0] ==0

# Clean Up
del smc100
