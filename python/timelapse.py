#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import threading
import socket
import errno
# python-gphoto2 - Python interface to libgphoto2
# import gphoto2 as gp
import commands
from time import sleep
execfile("/srv/git/timelapse/python/common/Functions.py")

#### GPIO DEFINITION ##################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#### PROGRAM DEFINITION ##################

# init list with pin numbers

frontMotor = Motor([21,20,16,12])
frontMotor.rpm = 10

backMotor = Motor([26,19,13,6])
backMotor.rpm = 1

# Application variables

SOCKET_FILE = "/var/run/python_timelapse_socket"
LOG_FILE = "/var/log/timelapse.log"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# default values / car commands
forward = 0				# speed parameters (positive forward, negative backward, 0 means stop)
shootingInterval = 0	# camera shooting interval
exit = False;			# stop flag for while loop

### Setup the camera. Set the capture tarrget to memory card

#log(os.system("gphoto2 --get-config capturetarget"))

###################### FUNCTIONS ######################

### Socket definition and read mechanism
def readSocket():
	global msg
	
	print("Opening socket...")
	usocket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	usocket.bind(SOCKET_FILE)
	os.chmod(SOCKET_FILE, 0777)
	print("Listening...")
	while True:
		msg = usocket.recv(1024)
		handleMessage(msg)
		time.sleep(0.1)

### Handle the messages command from outside
def handleMessage(msg):
	
	global forward, shootingInterval
	
	# message could contain more command in comma separated value
	if not msg == "":
	    command,value = msg.split(",")
	else:
	    command = ""

	## Set ALL values and the contorl the cas

	############## speed ################
	if (command == 'move'):
		if (value == 'forward'):
			forward = 1;
			log("Move forward")
		if (value == 'backward'):
			forward = -1
			log("Move backward")
		if (value == 'stop'):
			forward = 0
			log("Stop move")
		
	############## direction ############

	if (command == 'turn'):
		if (value == 'left'):
			frontMotor.move_to(35)
			log("Turn left")
		if (value == 'right'):
			frontMotor.move_to(-35);
			log("Turn right")
		if (value == 'straight'):
			frontMotor.move_to(0);
			log("Back to straight")
		
	############## fine tune ############	    

	if (command == 'fine'):
		if (value == 'left'):
			frontMotor.step(1)
			log("Fine tune left")
		if (value == 'right'):
			frontMotor.step(-1)
			log("Fine tune right")
	
	########## shooting time ############
	if (command == 'shoot'):
		shootingInterval = int(value)
		log("Shooting interval set to " + value)

	# always set to emty the msg if that was processed
	if not command == "":
	    msg = ""

### Fires the camera
### in another thread because of the periodic loop
def fireCamera():
    
    # Read the interval from global variable. 0 means do not fire the camrea, we don't lose the timer if t=0
    t = int(shootingInterval)
    threading.Timer(t, fireCamera).start()
    
    if (t != 0):
	os.system("gphoto2 --set-config capturetarget=1")
	log(str(commands.getstatusoutput('gphoto2 --get-config capturetarget')))
	commands.getstatusoutput('gphoto2 --trigger-capture')
		
## Log the given message
def log(msg):
	f = open(LOG_FILE,'a')
	f.write(time.strftime(TIME_FORMAT) + " - " + msg + "\n")
	f.close()
    
###################### FUNCTIONS END ######################

### Delete the socket file from the previous session to the clear system
if os.path.exists(SOCKET_FILE):
    os.remove(SOCKET_FILE)

### Create a log file if not exists
if (not os.path.isfile(LOG_FILE)):
	f = open(LOG_FILE,'w')
	f.write(time.strftime(TIME_FORMAT) + " - Log started")
	f.close()

############# Camera fire ##########
# run the camera fire process (external) first and then step into the main loop to move the car
fireCamera()

# read the socket with another thread
threading.Thread(target=readSocket).start()

# main loop
try:
  while True and not exit:
		
	backMotor.step(forward);
	
	if forward == 0:
	    time.sleep(1)

# End program cleanly with keyboard
except KeyboardInterrupt:
	print "  Quit"
	exit = True;

# Reset GPIO settings
GPIO.cleanup()


