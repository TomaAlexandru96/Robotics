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
motorParams0.maxRotationAcceleration = 5.0
motorParams0.maxRotationSpeed = 11.0
motorParams0.feedForwardGain = 13.45
motorParams0.minPWM = 25
motorParams0.pidParameters.minOutput = -255
motorParams0.pidParameters.maxOutput = 255
motorParams0.pidParameters.k_p = 670.0
motorParams0.pidParameters.k_i = 200.0
motorParams0.pidParameters.k_d = 0.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 5.0
motorParams1.maxRotationSpeed = 11.0
motorParams1.feedForwardGain = 13.3
motorParams1.minPWM = 25
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 730.0
motorParams1.pidParameters.k_i = 160.0
motorParams1.pidParameters.k_d = 0.0

interface.setMotorAngleControllerParameters(motors[0], motorParams0)
interface.setMotorAngleControllerParameters(motors[1], motorParams1)

interface.startLogging("logfile.txt")
while True:
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
