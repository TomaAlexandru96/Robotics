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




theta = 0
k_l = 15
k_r = 15




# Timestep delta to run control and simulation at
dt = 0.01

# Barrier (obstacle) locations
barriers = []
# barrier contents are (bx, by, visibilitymask)
# Generate some initial random barriers
#for i in range(2):
#    (bx, by) = (random.uniform(PLAYFIELDCORNERS[0], PLAYFIELDCORNERS[2]), random.uniform(PLAYFIELDCORNERS[1], PLAYFIELDCORNERS[3]))
#    barrier = [bx, by, 0]
#    barriers.append(barrier)

def newObstacle():
    average = 0
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading > 5:
            average = average + reading
    average = average / 5.0
    if average < 50:
        print(average)
        return average
    return 100000.0

def setSpeed(vL, vR):
    interface.setMotorPwm(robotConfigVel.motors[0],vR)
    interface.setMotorPwm(robotConfigVel.motors[1],vL)     

def obstacleDetected():
    global turnAround
    if (newObstacle() < 45):
        print('AVOIDING OBSTACLE')
        turnAround = False
        return True
        
    return False
        
    
def turnLeftSharp(destAngle):
    global initialDifference, k_l, interface
    setSpeed(0, 200)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_l < destAngle):
        #print(diff)
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)

    
def turnRightSharp(destAngle):
    global initialDifference, k_r, interface
    setSpeed(200, 0)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_r > destAngle):
        #print(diff)
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)
        
        
def turnLeftSlow(destAngle):
    global initialDifference, k_l, interface
    setSpeed(85, 210)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_l < destAngle):
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)
        
        
def turnRightSlow(destAngle):
    global initialDifference, k_l, interface
    setSpeed(210, 85)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_r > destAngle):
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)

def turnRightSlowCheck(destAngle):
    global initialDifference, k_r, interface
    setSpeed(100, 50)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_r > destAngle):
        if (obstacleDetected()):
            print('OBTACLE DETECTED BREAK')
            break
        motorAngles = interface.getMotorAngles(robotConfigVel.motors)
        diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
        time.sleep(dt)

def turnLeftSlowCheck(destAngle):
    global initialDifference, k_l, interface
    setSpeed(50, 100)
    motorAngles = interface.getMotorAngles(robotConfigVel.motors)
    diff = motorAngles[0][0] - motorAngles[1][0] - initialDifference
    while(diff * k_l < destAngle):
        if (obstacleDetected()):
            print('OBTACLE DETECTED BREAK')
            break
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
        
        setSpeed(90,90)
        average = 0
        for i in range(0,5):
            (reading, _) = interface.getSensorValue(3)
            average = average + reading
        average = average / 5.0
        while(average > 25):
            average = 0
            for i in range(0,5):
                (reading, _) = interface.getSensorValue(3)
                average = average + reading
            average = average / 5.0
            if average > 50 and average < 200:
                if turningLeft:
                    turnRightSharp(0)
                else:
                    turnLeftSharp(0)
                turnAround = False
                continue
        print(average)
        #time.sleep(minReading * 0.015)
        if turningLeft:
            print('TURN LEFT')
            turnLeftSharp(90)

            print('TURN RIGHT, CHECK ON SECOND HALF')
            turnRightSlow(0)
            motorAngles = interface.getMotorAngles(robotConfigVel.motors)
            initialDifference = motorAngles[0][0] - motorAngles[1][0]
            turnRightSlowCheck(-45)
            
            turningLeft = False
            
            # Continue going straight after detecting obstacle
            if not(turnAround):
                turnAround = True
                print('STOP TURNING LEFT START NEW TURNING')
                continue
            
            print('TURN TO 0')
            #initialDifference = initialDifference - 1
            turnLeftSharp(-20)
            motorAngles = interface.getMotorAngles(robotConfigVel.motors)
            initialDifference = motorAngles[0][0] - motorAngles[1][0]
        else:
            print('TURN RIGHT')
            turnRightSharp(-90)
            
            print('TURN LEFT, CHECK ON SECOND HALF')
            turnLeftSlow(0)
            motorAngles = interface.getMotorAngles(robotConfigVel.motors)
            initialDifference = motorAngles[0][0] - motorAngles[1][0]
            turnLeftSlowCheck(45)
            
            turningLeft = True
            
            # Continue going straight after detecting obstacle
            if not(turnAround):
                turnAround = True
                print('STOP TURNING RIGHT START NEW TURNING')
                continue
            
            print('TURN TO 0')
            #initialDifference = initialDifference + 1
            turnRightSharp(10)
            motorAngles = interface.getMotorAngles(robotConfigVel.motors)
            initialDifference = motorAngles[0][0] - motorAngles[1][0]
        
        if not(turnAround):
            turnAround = True
            continue
        turnAround = False
    
    setSpeed(160,160)
    if obstacleDetected():
        turnAround = True
    #turnLeftSharp(90)
    #turnRightSharp(0)
    #break
    time.sleep(dt)
