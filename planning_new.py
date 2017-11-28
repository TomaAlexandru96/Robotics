# Planning
# Dynamic Window Approach (Local Planning)
# Andrew Davison 2017
import pygame, os, math, time, random, brickpi, robotConfigVel

# Constants and variables
# Units here are in metres and radians using our standard coordinate frame
BARRIERRADIUS = 0.06
ROBOTRADIUS = 0.06
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


# Barrier (obstacle) locations
barriers = []
# barrier contents are (bx, by, visibilitymask)
# Generate some initial random barriers
#for i in range(2):
#    (bx, by) = (random.uniform(PLAYFIELDCORNERS[0], PLAYFIELDCORNERS[2]), random.uniform(PLAYFIELDCORNERS[1], PLAYFIELDCORNERS[3]))
#    barrier = [bx, by, 0]
#    barriers.append(barrier)



# Constants for graphics display
# Transformation from metric world frame to graphics frame
# k pixels per metre
# Horizontal screen coordinate:     u = u0 + k * x
# Vertical screen coordinate:       v = v0 - k * y

# set the width and height of the screen (pixels)
WIDTH = 1500
HEIGHT = 1000

size = [WIDTH, HEIGHT]
black = (20,20,40)
lightblue = (0,120,255)
darkblue = (0,40,160)
red = (255,100,0)
white = (255,255,255)
blue = (0,0,255)
k = 160 # pixels per metre for graphics

# Screen centre will correspond to (x, y) = (0, 0)
u0 = WIDTH / 2
v0 = HEIGHT / 2




# Initialise Pygame display screen
#screen = pygame.display.set_mode(size)
# This makes the normal mouse pointer invisible in graphics window
#pygame.mouse.set_visible(0)


# Array for path choices use for graphics 
pathstodraw = []






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

# Function to calculate the closest obstacle at a position (x, y)
# Used during planning
def calculateClosestObstacleDistance(x, y):
    closestdist = 100000.0    
    # Calculate distance to closest obstacle
    for barrier in barriers:
        # Is this a barrier we know about? barrier[2] flag is set when sonar observes it
        #if(barrier[2] == 1):
        #print(x)
        #print(y)
        dx = barrier[0] - x
        dy = barrier[1] - y
        d = math.sqrt(dx**2 + dy**2)
        # Distance between closest touching point of circular robot and circular barrier
        dist = d - BARRIERRADIUS - ROBOTRADIUS
        if (dist < closestdist):
            closestdist = dist
    #print('minimum distance: ', closestdist)
    return closestdist

# Draw the barriers on the screen
def drawBarriers(barriers):
    for barrier in barriers:
        # Dark barriers we haven't seen
        if(barrier[2] == 0):
            pygame.draw.circle(screen, darkblue, (int(u0 + k * barrier[0]), int(v0 - k * barrier[1])), int(k * BARRIERRADIUS), 0)
        # Bright barriers we have seen
        else:
            pygame.draw.circle(screen, lightblue, (int(u0 + k * barrier[0]), int(v0 - k * barrier[1])), int(k * BARRIERRADIUS), 0)
    return

# Simulation of forward looking depth sensor; assume cone beam
# Which barriers can it see? If a barrier has been seen at least once it becomes known to the planner
SENSORRANGE = 1.5
def observeBarriers(x, y, theta):
    min_reading = 100000.0  
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        reading = reading - 12
        if reading < min_reading and reading > 20:
            min_reading = reading
    if min_reading < 100 and min_reading > 20:
        #print('OBSTACLE!!!!')
        #print('away: ', min_reading)
        #print('my x: ', x)
        #print('my y: ', y)
        #print('my theta: ', theta)
        barrier = [x + (math.cos(theta) * min_reading)*0.01 , y + (math.sin(theta) * min_reading)*0.01, 1]
        #print(barrier[0], barrier[1])
        barriers.append(barrier)
    #for i, barrier in enumerate(barriers):   
        #vector = (barrier[0] - x, barrier[1] - y)
        #vectorlength = math.sqrt(vector[0]**2 + vector[1]**2)
        #barrierangularhalfwidth = BARRIERRADIUS / vectorlength 
        #if(vectorlength < SENSORRANGE):
            #barriers[i][2] = 1
# Simulation of forward looking depth sensor; assume cone beam
# Which barriers can it see? If a barrier has been seen at least once it becomes known to the planner
SENSORRANGE = 1.5
def newObstacle(x, y, theta):
    min_reading = 100000.0
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        print(reading)
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
    return [];

def setSpeed(vL, vR):
    #print(theta * 180 / math.pi)
    #print(x)
    interface.setMotorRotationSpeedReferences(robotConfigVel.motors,[vR * 30,vL * 30])
            
interface = brickpi.Interface()
interface.initialize()


robotConfigVel.configureRobot(interface)
interface.sensorEnable(3, brickpi.SensorType.SENSOR_ULTRASONIC)
turnAround = False
currentObstacle = []
# Main loop
while(1):
    # Planning

    #print "New action"
    pathstodraw = [] # We will store path details here for plotting later
    newpositionstodraw = [] # Also for possible plotting of robot end positions

    k = 0
    # Predict new position in TAU seconds
    TAU = 1.0 
    if turnAround:
        print('GET CLOSER')
        print('my x', x)
        print('obstacle x', currentObstacle[0])
        print('distance', abs(x - currentObstacle[0]))
        vL = 0.1
        vR = 0.1
        dx = x - currentObstacle[0]
        dy = y - currentObstacle[1]
        dist = math.sqrt(dx**2 + dy**2)
        setSpeed(vL, vR)
        while(dist > 0.3):
            print("Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            time.sleep(dt)
            dx = x - currentObstacle[0]
            dy = y - currentObstacle[1]
            dist = math.sqrt(dx**2 + dy**2)
        vL = 0.0
        vR = 0.2
        print(theta * 180 / math.pi)
        print('TURN LEFT')
        setSpeed(vL, vR)
        while(theta < 70 * math.pi / 180.0):
            print("Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            time.sleep(dt)
        vL = 0.2
        vR = 0.1
        print(theta * 180 / math.pi)
        print('TURN RIGHT')
        setSpeed(vL, vR)
        #print(theta)
        while(theta > 0):
            print("Position: " + str((x, y)) + "; Velocities: " + str((vL, vR)) + "; Theta: " + str(theta) + "; DT: " + str(dt))
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            #print('turning right')
            #print(vL)
            #print(vR)
            time.sleep(dt * 1.5)
        
        print(theta * 180 / math.pi)
        #k += 1
        #if k == 3:
        #    break
        
        
        print(theta * 180 / math.pi)
        print('TURN RIGHT WHILE CHECKING')
        while(theta > -45 * math.pi / 180.0):
            print(theta * 180 / math.pi)
            #print('turning right 2')
            new_obstacle = newObstacle(x,y,theta)
            if len(new_obstacle) > 0:
                dx = new_obstacle[0] - x
                dy = new_obstacle[1] - y
                distanceToObstacle = math.sqrt(dx**2 + dy**2)
            else:
                distanceToObstacle = 100000.0
            if (distanceToObstacle < 0.60):
                print('AVOIDING OBSTACLE 2')
                #print('distance to obstacle: ', distanceToObstacle)
                currentObstacle = new_obstacle
                turnAround = False
                break;
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            #print(vL)
            #print(vR)
            setSpeed(vL, vR)
            time.sleep(dt * 1.5)
        if not(turnAround):
            turnAround = True
            vL = 0.1
            continue
        
        print(theta * 180 / math.pi)
        
        print(theta * 180 / math.pi)
        print('TURN TO 0')
        vL = 0.1
        vR = 0.2
        while(theta < 0):
            #print('turning to 0 checking')
            new_obstacle = newObstacle(x,y,theta)
            if len(new_obstacle) > 0:
                dx = new_obstacle[0] - x
                dy = new_obstacle[1] - y
                distanceToObstacle = math.sqrt(dx**2 + dy**2)
            else:
                distanceToObstacle = 100000.0
            if (distanceToObstacle < 0.60):
                print('AVOIDING OBSTACLE 2')
                print('distance to obstacle: ', distanceToObstacle)
                currentObstacle = new_obstacle
                turnAround = False
                break;
            (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
            #print(vL)
            #print(vR)
            setSpeed(vL, vR)
            time.sleep(dt * 1.3)
        if not(turnAround):
            turnAround = True
            continue
        print(theta * 180 / math.pi)
        vL = 0.1
        vR = 0.1
        turnAround = False
        
            
    new_obstacle = newObstacle(x,y,theta)
    if len(new_obstacle) > 0:
        dx = new_obstacle[0] - x
        dy = new_obstacle[1] - y
        distanceToObstacle = math.sqrt(dx**2 + dy**2)
    else:
        distanceToObstacle = 100000.0
    if (distanceToObstacle < 0.60):
        currentObstacle = new_obstacle
        print('AVOIDING OBSTACLE 1')
        print('distance to obstacle: ', distanceToObstacle)
        turnAround = True
        continue
    
    # END PLANNING
    vR = 0.1
    vL = 0.1
    (x, y, theta) = predictPosition(vL, vR, x, y, theta, dt)
    #print(vL)
    #print(vR)
    setSpeed(vL, vR)

    # Sleeping dt here runs simulation in real-time
    time.sleep(dt)
