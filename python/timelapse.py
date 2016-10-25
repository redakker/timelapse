#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import threading
import socket
import errno
from time import sleep
execfile("common/Functions.py")

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
msg = ""				#commands is written to this variable
forward = 0				# speed parameters (positive forward, negative backward, 0 means stop)
# direction = 0 		# direction of the car (1=right, 0=straight, -1=left)
# fineTune = 0    		# fine tune the front motor (1=right, -1=left)
shootingInterval = 0	# camera shooting interval

# Create socket for communication between the web and python

if os.path.exists(SOCKET_FILE):
    os.remove(SOCKET_FILE)

print("Opening socket...")
usocket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
usocket.bind(SOCKET_FILE)
usocket.setblocking(0)
os.chmod(SOCKET_FILE, 0777)
print("Listening...")
	

if (not os.path.isfile(LOG_FILE)):
	f = open(LOG_FILE,'w')
	f.write(time.strftime(TIME_FORMAT) + " - Log started")
	f.close()
###################### FUNCTIONS

def fireCamera():
    timer = 1
    # Read the interval from global variable. 0 means do not fire the camrea, we don't lose the timer if t=0
    #t = int(shootingInterval)
    #threading.Timer(t, fireCamera).start()
    
    #if (t != 0):
	#print "shoot"
    
def log(msg):
	f = open(LOG_FILE,'a')
	f.write(time.strftime(TIME_FORMAT) + " - " + msg + "\n")
	f.close()
	
    
###################### FUNCTIONS END

############# camera fire ##########

# run the camera fire process (external) first and then step into the main loop to move the car
fireCamera()

# main loop
try:
  while True:
	
	try:
		msg = usocket.recv(1024)
	except socket.error:
		print "no data"
		
	print "lefut"
	if not msg:
		break
	else:
		log(msg)
		if "QUIT" == msg:
			log("QUIT command received, program exit")
			break

	# message could contain more command in comma separated value
	command,value = msg.split(",")

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
			
	backMotor.step(forward);
		
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
	msg = ""

# End program cleanly with keyboard
except KeyboardInterrupt:
	print "  Quit"

# Reset GPIO settings
GPIO.cleanup()


