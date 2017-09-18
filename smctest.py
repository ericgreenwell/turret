from smc100 import *

smc100 = SMC100(1, "/dev/tty5", silent=False)

print smc100.get_position_mm()

smc100.home()

#make sure there are no errors

assert smc100.get_status()[0] == 0

pos = smc100.get_position_mm()

smc.move_absolute_mm(5)

assert smc100.get_status()[0] ==0

del smc100
