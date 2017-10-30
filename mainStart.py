import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

right = 3
left = 1

motors = [left, right]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams0 = interface.MotorAngleControllerParameters()
motorParams0.maxRotationAcceleration = 4.0
motorParams0.maxRotationSpeed = 10.0
motorParams0.feedForwardGain = 13.17
motorParams0.minPWM = 25
motorParams0.pidParameters.minOutput = -255
motorParams0.pidParameters.maxOutput = 255
motorParams0.pidParameters.k_p = 570.0
motorParams0.pidParameters.k_i = 195.0
motorParams0.pidParameters.k_d = 30.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 4.0
motorParams1.maxRotationSpeed = 10.0
motorParams1.feedForwardGain = 13.12
motorParams1.minPWM = 25
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 570.0
motorParams1.pidParameters.k_i = 195.0
motorParams1.pidParameters.k_d = 30.0

interface.setMotorAngleControllerParameters(motors[0], motorParams0)
interface.setMotorAngleControllerParameters(motors[1], motorParams1)

angle90=3.2
length40=11.55

def goStraight40cm():
	interface.increaseMotorAngleReferences(motors,[length40,length40])
	while not interface.motorAngleReferencesReached(motors):
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)
	return

def turnLeft90():
	interface.increaseMotorAngleReferences(motors,[-angle90,angle90])
	while not interface.motorAngleReferencesReached(motors):
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)	
	return

def turnRight90():
	interface.increaseMotorAngleReferences(motors,[angle90,-angle90])
	while not interface.motorAngleReferencesReached(motors):
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)	
	return
		

interface.startLogging("logfile.txt")
while True:
        square = bool(input("Do you want to draw a square?: "))

        if square:
		for x in range(3):
			goStraight40cm()
			turnLeft90()
		goStraight40cm()
	else:
		angle0 = float(input("Enter a angle to rotate 0 (in radians): "))
        	angle1 = float(input("Enter a angle to rotate 1 (in radians): "))

		interface.increaseMotorAngleReferences(motors,[angle0,angle1])

		while not interface.motorAngleReferencesReached(motors) :
			motorAngles = interface.getMotorAngles(motors)
			if motorAngles :
				print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
			time.sleep(0.1)

		print "Destination reached!"
	

interface.stopLogging()
interface.terminate()
