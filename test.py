import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
step_1 = 13
dir_1 = 19

GPIO.setup(dir_1, GPIO.OUT)

GPIO.setup(step_1, GPIO.OUT)


while True:
    try:
        GPIO.output(dir_1, True)
        GPIO.output(step_1,True)
        GPIO.output(step_1,False)
        time.sleep(.001)

    except KeyboardInterrupt:
        pass


exit()
