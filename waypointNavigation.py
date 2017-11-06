import math
import mainStart

robotPosition = [0, 0, 0]

def rotateRobot(angle):
    print("Rotating " + angle)
    pass


def goStraight(distance):
    print("Moving " + distance)
    pass


def navigateToWaypoint(x, y):
    dx = x - robotPosition[0]
    dy = y - robotPosition[1]
    alpha = math.atan2(dy, dx)

    beta = alpha - robotPosition[2]

    if beta <= -math.pi:
        beta += 2*math.pi
    elif beta > math.pi:
        beta -= 2*math.pi

    rotateRobot()
    goStraight(math.sqrt(dx * dx + dy * dy))

    robotPosition[0] = x
    robotPosition[1] = y
    robotPosition[2] = alpha

while True:
    x = float(input("x="))
    y = float(input("y="))
    navigateToWaypoint(x, y)
