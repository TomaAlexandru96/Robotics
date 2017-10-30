import brickpi
import time
import robotConfig

interface = brickpi.Interface()

angle90 = 3.2
length40 = 11.55

def driveUntilReferenceAnglesReached(angles):
    interface.increaseMotorAngleReferences(robotConfig.motors, angles)

    while not interface.motorAngleReferencesReached(robotConfig.motors):
        motorAngles = interface.getMotorAngles(robotConfig.motors)

        if motorAngles:
            print("Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0])

        time.sleep(0.1)

def askForReferenceAngles():
    angle0 = float(input("Enter a angle to rotate 0 (in radians): "))
    angle1 = float(input("Enter a angle to rotate 1 (in radians): "))

    driveUntilReferenceAnglesReached([angle0,angle1])

    print("Destination reached!")

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

def main():
    interface.initialize()
    # interface.startLogging("logfile.txt")

    robotConfig.configureRobot(interface)

    # interface.stopLogging()
    interface.terminate()

if __name__ == "__main__":
    main()
