import math
import robot

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

    robot.initInterfaceAndRun(lambda: robot.rotate(beta), robot.goStraight(math.sqrt(dx * dx + dy * dy)))

    robotPosition[0] = x
    robotPosition[1] = y
    robotPosition[2] = alpha


while True:
    x = float(input("x="))
    y = float(input("y="))
    navigateToWaypoint(x, y)
