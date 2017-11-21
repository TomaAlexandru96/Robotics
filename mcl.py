import particleDataStructures
import math
import random
import time
import sys
import brickpi
import robotConfig
straight20 = 5.75
rotationConstant = 2.13

def goStraight(distance):
    distance = (distance / 20.0) * straight20
    driveUntilReferenceAnglesReached([distance, distance])

def rotate(angle):
    driveUntilReferenceAnglesReached([angle * rotationConstant, -angle * rotationConstant])

def driveUntilReferenceAnglesReached(angles):
    interface.increaseMotorAngleReferences(robotConfig.motors, angles)

    while not interface.motorAngleReferencesReached(robotConfig.motors):
        motorAngles = interface.getMotorAngles(robotConfig.motors)

    #
    if motorAngles: #print("Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0])

        time.sleep(0.1)


def askForReferenceAngles():
    angle0 = float(input("Enter a angle to rotate 0 (in radians): "))
    angle1 = float(input("Enter a angle to rotate 1 (in radians): "))

    driveUntilReferenceAnglesReached([angle0, angle1])

    print("Destination reached!")

def resample(particles):
    n = len(particles)
    weight_sum = 0
    cumulative_weights = [0] * n
    i = 0
    for (x, y, theta, w) in particles:
        weight_sum += w
        cumulative_weights[i] = weight_sum
        i = i + 1

    # print(cumulative_weights)

    new_particle_set = [(0, 0, 0, 0)] * n
    for n_i, (x, y, theta, w) in enumerate(new_particle_set):
        r = random.uniform(0, 1);
        r_particle_index = 0;
        for cw_i, weight in enumerate(cumulative_weights):
            if r <= weight:
                (x_old, y_old, theta_old, w_old) = particles[cw_i]
                new_particle_set[n_i] = (x_old, y_old, theta_old, weight_sum / (n * 1.0))
                break


    return new_particle_set


def normalise(particles):
    tot_weight = 0
    for (x, y, theta, w) in particles:
        tot_weight += w
        i = 0
    for (x, y, theta, w) in particles:
        particles[i] = (x, y, theta, w / (tot_weight * 1.0))
        i = i + 1;
    return particles


def calculate_likelihood(x, y, theta, w, z):
    for i, wall in enumerate(mymap.walls):
        wallName = chr(ord('a') + i)

        # print(wallName)
        (Ax, Ay, Bx, By) = wall

        numerator = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)

        denominator = (By - Ay) * math.cos(theta) - (Bx - Ax) * math.sin(theta)
        if denominator == 0:
            continue
        m = numerator / denominator

        # print("m: " + str(m))

        if m < 0:
            continue

        (hitX, hitY) = (x + m * math.cos(theta), y + m * math.sin(theta))#(Ax, Ay) = (max(Ax, Bx), max(Ay, By))
        firstAX = min(Ax, Bx)
        lastAX = max(Ax, Bx)
        firstAY = min(Ay, By)
        lastAY = max(Ay, By)

        # print("Wall: " + str((firstAX, lastAX)) + " - " + str((firstAY, lastAY)))# print("hitX, hitY: " + str((hitX, hitY)))

        if (firstAX < hitX or isclose(firstAX, hitX)) and(hitX < lastAX or isclose(lastAX, hitX)) and(firstAY < hitY or isclose(firstAY, hitY)) and(hitY < lastAY or isclose(lastAY, hitY)): #print("Wall hit: " + wallName)
            break


    a = math.cos(theta) * (Ay - By) + math.sin(theta) * (Bx - Ax)
    b = math.sqrt(math.pow(Ay - By, 2) + math.pow(Bx - Ax, 2))
    incidence = math.acos(a / b)

    
    if incidence > math.pi / 18.0:
        return w


    numerator = -(math.pow((z - m), 2))
    denominator = 2 * math.pow(1.5, 2)
    pzm = math.exp(numerator / denominator) + 0.02

    # print("PZM: " + str(pzm))
    return pzm * w



def isclose(a, b, rel_tol = 1e-09, abs_tol = 0.0001):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)



distance = 20
angleOfRotation = math.pi / 2

port = 3# port which ultrasoic sensor is plugged in to


c = 0;
def getNewX(x, e, theta, distance):
    x = x + (distance + e) * math.cos(theta)
    return x

def getNewY(y, e, theta, distance):
    y = y + (distance + e) * math.sin(theta)
    return y

def getNewThetaStraight(theta):
    theta = theta + getErrorRotation();
    return theta

def getNewThetaRotation(theta, alpha):
    global angleOfRotation;
    theta = theta + getErrorRotation() + alpha;
    return theta

def getNewThetaRotationLeft(theta):
    global angleOfRotation;
    theta = theta + getErrorRotation() + angleOfRotation;
    return theta

def getNewThetaRotationRight(theta):
    global angleOfRotation;
    theta = theta + getErrorRotation() - angleOfRotation;
    return theta

def getErrorRotation():
    return random.gauss(0, 0.015)

def getErrorStraight():
    return random.gauss(0, 0.4)



def getNextParticleStraight((x, y, theta, w), distance):
    e = getErrorStraight();
    (reading, _) = interface.getSensorValue(3)
    reading = reading - 12
    return (getNewX(x, e, theta, distance), getNewY(y, e, theta, distance), getNewThetaStraight(theta), calculate_likelihood(x, y, theta, w, reading))

def getNextParticleRotation((x, y, theta, w), alpha):
    (reading, _) = interface.getSensorValue(3)
    reading = reading - 12
    return (x, y, getNewThetaRotation(theta, alpha), calculate_likelihood(x, y, theta, w, reading))


mymap = particleDataStructures.Map();

mymap.add_wall((0, 0, 0, 168));#

mymap.add_wall((0, 168, 84, 168));#

mymap.add_wall((84, 126, 84, 210));#

mymap.add_wall((84, 210, 168, 210));#

mymap.add_wall((168, 210, 168, 84));#

mymap.add_wall((168, 84, 210, 84));#

mymap.add_wall((210, 84, 210, 0));#

mymap.add_wall((210, 0, 0, 0));#


interface = brickpi.Interface()
interface.initialize()
numberOfParticles = 100


robotConfig.configureRobot(interface)
interface.sensorEnable(3, brickpi.SensorType.SENSOR_ULTRASONIC);

myCanvas = particleDataStructures.Canvas();

waypoints = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]


mymap.draw();

x = 84
y = 30
theta = 0.0
w = 1 / (numberOfParticles * 1.0)
initialParticles = [(x, y, theta, w) for _ in range(numberOfParticles)]
particles = initialParticles# print('initial particles')

def main():
    global x
    global y
    global theta
    global particles
    global myCanvas
    myCanvas.drawParticles(initialParticles)

    for (x2, y2) in waypoints:
        reached = False
        while not reached:
            dx = x2 - x
            dy = y2 - y
            distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
            if distance > 20:
                distance = 20
            else :
                reached = True# print(distance)

            alpha = math.atan2(dy, dx)
            if alpha > math.pi:
                alpha = alpha - (math.pi * 2)
            if alpha < (-math.pi):
                alpha = alpha + (math.pi * 2)


            angle_of_rotation = alpha - theta
            if angle_of_rotation > math.pi:
                angle_of_rotation = angle_of_rotation - (math.pi * 2)
            if angle_of_rotation < (-math.pi):
                angle_of_rotation = (math.pi * 2) + angle_of_rotation
            rotate(angle_of_rotation)

            particles = [getNextParticleRotation(p, angle_of_rotation) for p in particles]
            normalise(particles)
            resample(particles)


            goStraight(distance)


            particles = [getNextParticleStraight(p, distance) for p in particles]

            print('particles: ')
            print(particles)
            myCanvas.drawParticles(particles)

            time.sleep(0.2)
            
            normalise(particles)
            resample(particles)

            print('new particles: ')
            print(particles)
            myCanvas.drawParticles(particles)

            x_e_avg = 0
            y_e_avg = 0
            theta_e_avg = 0
            for (x_e, y_e, theta_e, w_e) in particles:
                x_e_avg = x_e_avg + x_e * w_e
                y_e_avg = y_e_avg + y_e * w_e
                theta_e_avg = theta_e_avg + theta_e * w_e
            x = x_e_avg
            y = y_e_avg
            if theta_e_avg > math.pi:
                theta = theta_e_avg - (math.pi * 2)
            elif theta_e_avg < (-math.pi):
                theta = theta_e_avg + (math.pi * 2)
            else :
                theta = theta_e_avg




def func(): ##Adding Waypoints
    mymap.add_wall((84, 30, 180, 30));
    mymap.add_wall((180, 30, 180, 54));
    mymap.add_wall((180, 54, 138, 54));
    mymap.add_wall((138, 54, 138, 168));
    mymap.add_wall((138, 168, 114, 168));
    mymap.add_wall((114, 168, 114, 84));
    mymap.add_wall((114, 84, 84, 84));
    mymap.add_wall((84, 84, 84, 30));


def test_likelihood():
    calculate_likelihood(2, 2, math.pi / 2, 1, 2)
    calculate_likelihood(2, 2, math.pi / 4, 1, 2)
    calculate_likelihood(2, 2, 0, 1, 2)
    calculate_likelihood(2, 2, -math.pi / 4, 1, 2)
    calculate_likelihood(2, 2, -math.pi / 2, 1, 2)
    calculate_likelihood(2, 2, -3 * math.pi / 4, 1, 2)
    calculate_likelihood(2, 2, math.pi, 1, 2)

main()