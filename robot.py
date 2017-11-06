import brickpi
import time
import robotConfig
import sys
import math

interface = brickpi.Interface()

angle90 = 3.20
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
    goStraight(length40)


def turnLeft90():
    rotate(-angle90)


def turnRight90():
    rotate(angle90)


def rotate(angle):
    driveUntilReferenceAnglesReached([angle, -angle])


def goStraight(distance):
    driveUntilReferenceAnglesReached([distance, distance])


def drawSquare():
    for x in range(3):
            goStraight40cm()
            turnLeft90()
    goStraight40cm()


def initInterface(withLog = False):
    interface.initialize()
    if withLog:
        interface.startLogging("logfile.txt")
    robotConfig.configureRobot(interface)


def stopInterface(withLog = False):
    if withLog:
        interface.stopLogging()
    interface.terminate()


robotPosition = [0, 0, 0]


def navigateToWaypoint(x, y):
    dx = x - robotPosition[0]
    dy = y - robotPosition[1]
    alpha = math.atan2(dy, dx)

    beta = alpha - robotPosition[2]

    if beta <= -math.pi:
        beta += 2*math.pi
    elif beta > math.pi:
        beta -= 2*math.pi

    rotate(beta)
    goStraight(math.sqrt(dx * dx + dy * dy))

    robotPosition[0] = x
    robotPosition[1] = y
    robotPosition[2] = alpha


def run():
    if sys.argv[1] == "1":
        goStraight40cm()
    elif sys.argv[1] == "2":
        turnLeft90()
    elif sys.argv[1] == "3":
        turnRight90()
    elif sys.argv[1] == "4":
        drawSquare()
    elif sys.argv[1] == "5":
        while True:
            x = float(input("x="))
            y = float(input("y="))
            navigateToWaypoint(x, y)


def main():
    initInterface()
    run()
    stopInterface()


if __name__ == "__main__":
    main()
