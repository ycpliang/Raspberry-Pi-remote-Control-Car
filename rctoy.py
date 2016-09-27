import RPi.GPIO as GPIO
import time
import pygame


#initiate
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
servo = GPIO.PWM(7,50)

ControlPin = [11,12,13,16]

for pin in ControlPin:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,0)

seq = [ [1,1,0,0],
	[0,1,1,0],
	[0,0,1,1],
	[1,0,0,1]]

pygame.init()
controlFailed = 0
done = False
servo.start(7.5)

# Initialize the joysticks
pygame.joystick.init()

def initiateStepper():
	for pin in ControlPin:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,0)

# helper function
def leftOrRightHandler(axis):
	dutyCycleVal = (axis + 1.5) * 5
	servo.ChangeDutyCycle(dutyCycleVal)
#	print("leftRIGHT value {}".format(dutyCycleVal))


def forwardOrBackHandler(axis):
#        print("forward and back value {}".format(axis))
	initiateStepper()
	for i in range(int(abs(axis) * 20)):
		for fullstep in range(4):
			for pin in range(4):
				if (axis >= 0):
					GPIO.output(ControlPin[pin], seq[fullstep][pin])
				else:
					GPIO.output(ControlPin[pin], seq[3 - fullstep][pin])
			time.sleep(0.002)

# -------- Main Program Loop -----------
while done == False: 

    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN $
#        if event.type == pygame.JOYBUTTONDOWN:
#            print("Joystick button pressed.")
#        if event.type == pygame.JOYBUTTONUP:
#            print("Joystick button released.")


    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
#    print("joystick Count {}".format(joystick_count))    

    #exit condition
    if(joystick_count == 0):
	if(controlFailed == 4):
		done = True
		break;
	else:	
		controlFailed = controlFailed + 1
		time.sleep(5)
		pygame.joystick.quit()
    		pygame.joystick.init()
	# For each joystick:
    else:
	joystick = pygame.joystick.Joystick(0)
    	joystick.init()        
        # Get the name from the OS for the controller/joystick
#        name = joystick.get_name()
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
#        axes = joystick.get_numaxes()
#	for i in range( axes ):
#  	    axis = joystick.get_axis( i )
#            print("Axis {} value: {:>6.3f}".format(i, axis) ) 

    	leftOrRightaxis = joystick.get_axis(0)
        leftOrRightHandler(leftOrRightaxis)
	
	forwardOrBackaxis = joystick.get_axis(1)
	forwardOrBackHandler(forwardOrBackaxis)

#        buttons = joystick.get_numbuttons()
        
#        for i in range( buttons ):
#            button = joystick.get_button( i )
	   
	if( joystick.get_button(0) == 1):
    	    done = True
#    time.sleep(1)
    time.sleep(0.01)    
servo.stop()
GPIO.cleanup()
