# Planning
# Dynamic Window Approach (Local Planning)
# Andrew Davison 2017
import pygame, os, math, time, random, brickpi, robotConfigVel

# Constants and variables
# Units here are in metres and radians using our standard coordinate frame
BARRIERRADIUS = 0.06
ROBOTRADIUS = 0.07
W = 2 * ROBOTRADIUS # width of robot
SAFEDIST = 0.35    # used in the cost function for avoiding obstacles

MAXVELOCITY = 2         #ms^(-1) max speed of each wheel
MAXACCELERATION = 1     #ms^(-2) max rate we can change speed of each wheel


# The region we will fill with obstacles
PLAYFIELDCORNERS = (-3.0, -3.0, 3.0, 3.0)

# Set an initial target location which is beyond the obstacles
target = (PLAYFIELDCORNERS[2] + 1.0, 0)

# Starting pose of robot
x = PLAYFIELDCORNERS[0] - 0.5
y = 0.0
theta = 0


# Timestep delta to run control and simulation at
dt = 0.005
vLBase = 0.2
vRBase = 0.2

# Barrier (obstacle) locations
barriers = []
# barrier contents are (bx, by, visibilitymask)
# Generate some initial random barriers
#for i in range(2):
#    (bx, by) = (random.uniform(PLAYFIELDCORNERS[0], PLAYFIELDCORNERS[2]), random.uniform(PLAYFIELDCORNERS[1], PLAYFIELDCORNERS[3]))
#    barrier = [bx, by, 0]
#    barriers.append(barrier)

# Function to predict new robot position based on current pose and velocity controls
# Uses time deltat in future
# Returns xnew, ynew, thetanew
# Also returns path. This is just used for graphics, and returns some complicated stuff
# used to draw the possible paths during planning. Don't worry about the details of that.
def predictPosition(vL, vR, x, y, theta, deltat):
    # Simple special cases
    # Straight line motion
    if (vL == vR): 
        #print('straight')
        xnew = x + vL * deltat * math.cos(theta)
        ynew = y + vL * deltat * math.sin(theta)
        thetanew = theta
    # Pure rotation motion
    elif (vL == -vR):
        #print('rotation')
        xnew = x
        ynew = y
        thetanew = theta + ((vR - vL) * deltat / W)
    else:
        #print("Current position: " + str((vL, vR, x, y, theta, deltat)))
        # Rotation and arc angle of general circular motion
        # Using equations given in Lecture 2
        R = W / 2.0 * (vR + vL) / (vR - vL)
        deltatheta = ((vR - vL) * deltat / W)
        xnew = x + R * (math.sin(deltatheta + theta) - math.sin(theta))
        ynew = y - R * (math.cos(deltatheta + theta) - math.cos(theta))
        thetanew = theta + deltatheta

    #print("Predicted position: " + str((xnew, ynew, thetanew)))

    return (xnew, ynew, thetanew)

def newObstacle():
    min_reading = 100000.0
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading < min_reading and reading > 5:
            min_reading = reading
    if min_reading < 100 and min_reading > 5:
        print(reading)
        return reading
    return 100000.0

def setSpeed(vL, vR):
    interface.setMotorPwm(robotConfigVel.motors[0],vR)
    interface.setMotorPwm(robotConfigVel.motors[1],vL)     

def obstacleDetected():
    global turnAround
    if (newObstacle() < 50):
        print('AVOIDING OBSTACLE')
        turnAround = False
        return True
        
    return False
        
    
def turnLeftSharp(destAngle):
    global initialDifference
    setSpeed(0, 150)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * 15 < destAngle):
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)

    
def turnRightSharp(destAngle):
    global initialDifference
    setSpeed(150, 0)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff *15 > destAngle):
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)
        
        
def turnLeftSlow(destAngle):
    global initialDifference
    setSpeed(85, 210)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff *15 < destAngle):
        #if (diff * 15 > destAngle/2):
            #if (obstacleDetected()):
                #print('OBTACLE DETECTED BREAK')
                #break
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)
        
        
def turnRightSlow(destAngle):
    global initialDifference
    setSpeed(210, 85)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff *15 > destAngle):
        #if (diff * 15 < destAngle/2):
            #if (obstacleDetected()):
                #print('OBTACLE DETECTED BREAK')
                #break
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)
        

        
def degToRad(deg):
    return deg * math.pi / 180
        
    
interface = brickpi.Interface()
interface.initialize()

robotConfigVel.configureRobot(interface)
interface.sensorEnable(3, brickpi.SensorType.SENSOR_ULTRASONIC)
turnAround = False
currentObstacle = []
turningLeft = True

motorAngles = interface.getMotorAngles(robotConfigVel.motors)
initialDifference = motorAngles[0][0] - motorAngles[1][0]

# Main loop
while(1):
    if turnAround:
        
        setSpeed(120,120)
        minReading = 60
        (reading, _) = interface.getSensorValue(3)
        if reading < minReading:
            minReading = reading
        while(minReading > 25):
            (reading, _) = interface.getSensorValue(3)
            if reading < minReading:
                minReading = reading
            if minReading > 50:
                turnAround = False
                continue
        print(minReading)
        #time.sleep(minReading * 0.015)
        if turningLeft:
            print('TURN LEFT')
            turnLeftSharp(90)

            print('TURN RIGHT, CHECK ON SECOND HALF')
            turnRightSlow(-90)
            turningLeft = False
            
            # Continue going straight after detecting obstacle
            if not(turnAround):
                turnAround = True
                print('STOP TURNING LEFT START NEW TURNING')
                continue
            
            print('TURN TO 0')
            print(initialDifference)
            motorAngles = interface.getMotorAngles(robotConfigVel.motors)
            currentDifference = motorAngles[0][0] - motorAngles[1][0]
            print(currentDifference)
            initialDifference = initialDifference - 1
            turnLeftSharp(0)
        else:
            print('TURN RIGHT')
            turnRightSharp(-90)
            
            print('TURN LEFT, CHECK ON SECOND HALF')
            turnLeftSlow(90)
            turningLeft = True
            
            # Continue going straight after detecting obstacle
            if not(turnAround):
                turnAround = True
                print('STOP TURNING RIGHT START NEW TURNING')
                continue
            
            print('TURN TO 0')
            initialDifference = initialDifference + 1
            turnRightSharp(0)
        
        if not(turnAround):
            turnAround = True
            continue
        turnAround = False
    
    setSpeed(120,120)

    if obstacleDetected():
        turnAround = True
    time.sleep(dt)
