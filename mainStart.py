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

def driveUntilReferenceAnglesReached(angles):
    interface.increaseMotorAngleReferences(motors,angles)
    while not interface.motorAngleReferencesReached(motors):
            motorAngles = interface.getMotorAngles(motors)
            if motorAngles :
                    print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
            time.sleep(0.1)
    return

def askForReferenceAngles():
    angle0 = float(input("Enter a angle to rotate 0 (in radians): "))
    angle1 = float(input("Enter a angle to rotate 1 (in radians): "))

    driveUntilReferenceAnglesReached([angle0,angle1])

    print "Destination reached!"

def goStraight40cm():
    driveUntilReferenceAnglesReached([length40,length40])

def turnLeft90():
    driveUntilReferenceAnglesReached([-angle90,angle90])

def turnRight90():
    driveUntilReferenceAnglesReached([angle90,-angle90])
		
def drawSquare():
    for x in range(3):
            goStraight40cm()
            turnLeft90()
    goStraight40cm()

# interface.startLogging("logfile.txt")



# interface.stopLogging()

interface.terminate()
