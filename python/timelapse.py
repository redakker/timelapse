#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import threading
from time import sleep
execfile("common/Functions.py")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#### PROGRAM DEFINITION ##################

# init list with pin numbers

frontMotor = Motor([21,20,16,12])
frontMotor.rpm = 10

backMotor = Motor([26,19,13,6])
backMotor.rpm = 1

# Application variables
position = 0
SleepTime = 2
storedDirection = '0'
fineTune = '0'

# Set the pins to default
#for i in pinList: 
#    GPIO.setup(i, GPIO.OUT) 
#    GPIO.output(i, GPIO.HIGH)

# Create commander files
# These files are the interface between the commander website and the program

# Forward, backward (0=stop, 1=forward, -1=backward)
f = open('/tmp/speed','w')
f.write('0') # python will convert \n to os.linesep
f.close()

# Left, Right (0=forward, 1=right, -1=left)
f = open('/tmp/direction','w')
f.write(storedDirection) # python will convert \n to os.linesep
f.close()

# Fine tune (1=right, -1=left)
f = open('/tmp/finetune','w')
f.write(fineTune) # python will convert \n to os.linesep
f.close()

# Shoot time (seconds)
f = open('/tmp/shoottime','w')
f.write(fineTune) # python will convert \n to os.linesep
f.close()

os.chmod('/tmp/speed', 0777)
os.chmod('/tmp/direction', 0777)
os.chmod('/tmp/finetune', 0777)
os.chmod('/tmp/shoottime', 0777)

###################### FUNCTIONS

def fireCamera():
    timer = 1
    # Read the interval from file. 0 means do not fire the camrea, we don't lose the timer if t=0
    file = open('/tmp/shoottime', 'r')
    timer = file.read()
    t = float(timer)
    threading.Timer(t, fireCamera).start()
    
    if (timer != '0'):
	print "shoot"
    

    #print "a"
    

###################### FUNCTIONS END

############# camera fire ##########

# run the camera fire process (external) first and then step into the main loop to move the car
fireCamera()

# main loop
try:
  while True:
	try:
	    ############## speed ################
	    file = open('/tmp/speed', 'r')
	    speed = file.read()

	    if (speed != '0'):
		s = int(speed)
		backMotor.step(s);  
	

	    ############## direction ############

	    file = open('/tmp/direction', 'r')
	    direction = file.read()

	    if (direction != '0'):
		if (direction != storedDirection):
		    if (direction == '1'):
			frontMotor.move_to(-35);
			storedDirection = '1'
	    
		    if (direction == '-1'):
			frontMotor.move_to(35)
			storedDirection = '-1'

	    if (direction == '0' and direction != storedDirection):
		storedDirection = '0'
    		frontMotor.move_to(0)

	    ############## fine tune ############	    

	    file = open('/tmp/finetune', 'r')
	    fineTune = file.read()

	    if (fineTune != '0'):
		if (fineTune == '1'):
		    frontMotor.step(-1)
		if (fineTune == '-1'):
		    frontMotor.step(1)

		# Set back the fine tune value to 0
		f = open('/tmp/finetune','w')
		f.write('0') # python will convert \n to os.linesep
		f.close()


	#time.sleep(SleepTime)   
	except ValueError:
	    #noop
	    print "noop"
	

# End program cleanly with keyboard
except KeyboardInterrupt:
  print "  Quit"

  # Reset GPIO settings
  GPIO.cleanup()



