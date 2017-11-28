import robot

def rotateBy(angle):
    driveUntilReferenceAnglesReached([0, 0, angle])

rot_angle = 2

def newObstacle(x, y, theta):
    min_reading = 100000.0
    rotateBy(rot_angle)
    # FIRST
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading < min_reading and reading > 20:
            min_reading = reading
    rotateBy(-rot_angle)
    rotateBy(-rot_angle)
    # SECOND
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading < min_reading and reading > 20:
            min_reading = reading
    rotateBy(rot_angle)
    # THIRD
    for i in range(0,5):
        (reading, _) = interface.getSensorValue(3)
        if reading < min_reading and reading > 20:
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
