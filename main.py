import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

right = 2
left = 1

motors = [left, right]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams0 = interface.MotorAngleControllerParameters()
motorParams0.maxRotationAcceleration = 6.0
motorParams0.maxRotationSpeed = 12.0
motorParams0.feedForwardGain = 255/20.0
motorParams0.minPWM = 30.0
motorParams0.pidParameters.minOutput = -255
motorParams0.pidParameters.maxOutput = 255
motorParams0.pidParameters.k_p = 450.0
motorParams0.pidParameters.k_i = 160.0
motorParams0.pidParameters.k_d = 4.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 6.0
motorParams1.maxRotationSpeed = 12.0
motorParams1.feedForwardGain = 255/20.0
motorParams1.minPWM = 30.0
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 450.0
motorParams1.pidParameters.k_i = 180.0
motorParams1.pidParameters.k_d = 5.0

interface.setMotorAngleControllerParameters(motors[0], motorParams0)
interface.setMotorAngleControllerParameters(motors[1], motorParams1)

interface.startLogging("logfile.txt")
while True:
	angle = float(input("Enter a angle to rotate (in radians): "))

	interface.increaseMotorAngleReferences(motors,[angle,angle])

	while not interface.motorAngleReferencesReached(motors) :
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)

	print "Destination reached!"
	

interface.stopLogging()
interface.terminate()
