import subprocess
import os

cam_found = False

subprocess.Popen('sudo modprobe -r uvcvideo', shell=True)

while True:
	if os.path.exists("/dev/video0"):
		print "camera found"
		break
	else:
		subprocess.Popen('sudo modprobe uvcvideo', shell=True)
		time.sleep(2)
		print "Try again"

