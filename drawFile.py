import time
import sys
import math
import random
import mainStart

x = 100
y = 100
theta = 0

distance = 100
angleOfRotation = math.pi/2


c = 0;
def getNewX(x,e,theta):
    x = x + (distance + e) * math.cos(theta)   
    return x
    
def getNewY(y,e,theta):
    y = y + (distance +e) * math.sin(theta)
    return y
    
def getNewThetaStraight(theta): 
    theta = theta + getError();
    return theta 
    
def getNewThetaRotation(theta):
    global angleOfRotation;
    theta = theta + getError() + angleOfRotation;
    return theta

def getError():
    return random.gauss(0,0.02) 



numberOfParticles = 100


line1 = (100, 100, 100, 500) # (x0, y0, x1, y1)
line2 = (100, 100, 500, 100)  # (x0, y0, x1, y1)
line3 = (500, 100 ,500, 500)  # (x0, y0, x1, y1)
line4 = (100, 500, 500, 500)  # (x0, y0, x1, y1)

print "drawLine:" + str(line1)
print "drawLine:" + str(line2)
print "drawLine:" + str(line3)
print "drawLine:" + str(line4)

def getNextParticleStraight((x,y,theta)):
    e = getError();
    return (getNewX(x,e,theta),getNewY(y,e,theta),getNewThetaStraight(theta))

def getNextParticleRotation((x,y,theta)):
    return (x,y,getNewThetaRotation(theta))
    
drawnParticles = []
    
def main():
    global x
    global y
    global theta
    global drawnParticles
    initialParticles = [(x, y,theta) for _ in range(numberOfParticles)]
    particles = initialParticles
    
    mainStart.main()
    
    for j in range(4):
        for i in range (4):
            mainStart.goStraight10cm()
            particles = [getNextParticleStraight(p) for p in particles]
            drawnParticles.append(particles)
            print "drawParticles:" + str(drawnParticles)
            time.sleep(0.3)

        mainStart.turnRight90()

        particles = [getNextParticleRotation(p) for p in particles]
        drawnParticles.append(particles)
        print "drawParticles:" + str(drawnParticles)
    
    
main()
    

    

