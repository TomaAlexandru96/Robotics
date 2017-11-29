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
dt = 0.02
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

def newObstacle(x, y, theta):
    min_reading = 100000.0
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading < min_reading and reading > 5:
            min_reading = reading
    if min_reading < 100 and min_reading > 5:
        bx = x + (math.cos(theta) * min_reading)*0.01
        by = y + (math.sin(theta) * min_reading)*0.01
        barrier = [bx, by, 1]
        for old_barrier in barriers:
                ddx = old_barrier[0] - barrier[0]
                ddy = old_barrier[1] - barrier[1]
                bdist = math.sqrt(ddx**2 + ddy**2)
                if (bdist < 0.40):
                    return []
        barriers.append(barrier)
        return barrier
    return []

def setSpeed(vL, vR):
    interface.setMotorRotationSpeedReferences(robotConfigVel.motors,[vR * 30,vL * 30])   

def obstacleDetected():
    global currentObstacle, x, y, theta, turnAround
    new_obstacle = newObstacle(x, y, theta)

    if len(new_obstacle) > 0:
        dx = new_obstacle[0] - x
        dy = new_obstacle[1] - y
        distanceToObstacle = math.sqrt(dx**2 + dy**2)

        if (distanceToObstacle < 0.60):
            print('AVOIDING OBSTACLE 2')
            currentObstacle = new_obstacle
            turnAround = False
            return True
        
    return False
        
        
def turnLeft(destTheta):
    global theta, x, y, vL, vR
    initialTheta = theta

    while(theta < destTheta):    
        #print("left Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
        # Accelerate till max speed or half-way
        if (theta < (destTheta + initialTheta) / 2 and vR < 0.4):
            vR = max(0.01, vR + 0.005)
            maxTheta = theta
        
        # Start decelerating from the point at which we should reach destination, decelerate till 0 
        if (theta >= destTheta - (maxTheta - initialTheta) and vR > 0.000):
            vR = max(0.01, vR - 0.005)
            
        setSpeed(vL, vR)
        time.sleep(dt)
        (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
        
def turnLeftFromStraight(destTheta):
    global theta, x, y, vL, vR
    initialTheta = theta

    while(theta < destTheta):    
        #print("left Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
        # Accelerate till max speed or half-way
        if (vL > 0):
            vL = vL - 0.005
        
        # Start decelerating from the point at which we should reach destination, decelerate till 0 
        if (theta >= destTheta - (destTheta - initialTheta)/2 and vR > 0.000):
            vR = max(0.01, vR - 0.0035)
            
        setSpeed(vL, vR)
        time.sleep(dt)
        (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)


def turnRight(destTheta):
    global theta, x, y, vL, vR
    initialTheta = theta

    while(theta > destTheta): 
        #print("right Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
        # Accelerate till max speed or half-way
        if (theta > (destTheta + initialTheta) / 2 and vL < 0.4):
            vL = max(0.01, vL + 0.005)
            maxTheta = theta
        
        # Start decelerating from the point at which we should reach destination, decelerate till 0 
        if (theta <= destTheta - (maxTheta - initialTheta) and vL > 0.000):
            vL = max(0.01, vL - 0.005)
            
        setSpeed(vL, vR)
        time.sleep(dt)
        (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)

def turnLeftSlowly(destTheta, breakOnCondition = False):
    global theta, x, y, vL, vR
    initialTheta = theta

    while(theta < destTheta):    
        if (breakOnCondition and obstacleDetected()):
            break
            
        #print("left Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
        # Accelerate till max speed or half-way
        if (theta < (destTheta + initialTheta) / 2 and vR < 0.4):
            vR = max(0.01, vR + 0.005)
            
            if vL < 0.2:
                vL = max(0.01, vL + 0.002)
                
            maxTheta = theta
        
        # Start decelerating from the point at which we should reach destination, decelerate till 0 
        if (theta >= destTheta - (maxTheta - initialTheta) and vR > 0.000):
            
            if vL > 0:
                vL = max(0.01, vL - 0.002)
            
            vR = max(0.01, vR - 0.005)
            
        setSpeed(vL, vR)
        time.sleep(dt)
        (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)           
        
def turnRightSlowly(destTheta, breakOnCondition = False):
    global theta, x, y, vL, vR
    initialTheta = theta
    
    while(theta > destTheta): 
        if (breakOnCondition and obstacleDetected()):
            break
        
        #print("right Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
        # Accelerate till max speed or half-way
        if (theta > (destTheta + initialTheta) / 2 and vL < 0.4):
            vL = max(0.01, vL + 0.005)
            
            if vR < 0.2:
                vR = max(0.01, vR + 0.002)
            
            maxTheta = theta
        
        # Start decelerating from the point at which we should reach destination, decelerate till 0 
        if (theta <= destTheta - (maxTheta - initialTheta) and vL > 0.000):
            
            if vR > 0:
                vR = max(0.01, vR - 0.002)
            
            vL = max(0.01, vL - 0.005)
            
        setSpeed(vL, vR)
        time.sleep(dt)
        (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
        
def degToRad(deg):
    return deg * math.pi / 180
        
    
interface = brickpi.Interface()
interface.initialize()

robotConfigVel.configureRobot(interface)
interface.sensorEnable(3, brickpi.SensorType.SENSOR_ULTRASONIC)
turnAround = False
currentObstacle = []

# Main loop
while(1):

    if turnAround:
        vL = vLBase
        vR = vRBase
        dx = x - currentObstacle[0]
        dy = y - currentObstacle[1]
        dist = math.sqrt(dx**2 + dy**2)
        setSpeed(vL, vR)
        while(dist > 0.3):
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            time.sleep(dt)
            dx = x - currentObstacle[0]
            dy = y - currentObstacle[1]
            dist = math.sqrt(dx**2 + dy**2)

        print('TURN LEFT')
        turnLeftFromStraight(degToRad(90))
        
        vR = 0
        
        print('TURN RIGHT')
        turnRightSlowly(degToRad(0))

        print('TURN RIGHT WHILE CHECKING')
        turnRightSlowly(degToRad(-90), True)
            
        # Continue going straight after detecting obstacle
        if not(turnAround):
            turnAround = True
            continue
        
        print('TURN TO 0')
        turnLeft(degToRad(0))
        
        #if not(turnAround):
        #    turnAround = True
        #    continue
            
        turnAround = False
    
    vL = vR = 0.2
    setSpeed(vL, vR)
    time.sleep(dt)
    (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)

    if obstacleDetected():
        turnAround = True
