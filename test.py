import time
#import RPi.GPIO as GPIO
from smc100 import *


smc100 = SMC100(1, '/dev/ttyUSB0', silent=False)
print smc100.get_position_mm()

smc100.home()

  # make sure there are no errors
assert smc100.get_status()[0] == 0

smc100.move_relative_um(5*1000)
smc100.move_relative_mm(5)

assert smc100.get_status()[0] == 0

pos = smc100.get_position_mm()

assert abs(pos-10)<0.001

smc100.move_relative_mm(-pos)

assert smc100.get_status()[0] == 0

del smc100
