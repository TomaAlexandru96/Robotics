motor_right = 3
motor_left = 1
touch_sensor_left = 4
touch_sensor_right = 5

motors = [motor_left, motor_right]

def configureRobot(interface):
    motorParams0 = interface.MotorAngleControllerParameters()
    motorParams0.maxRotationAcceleration = 4.0
    motorParams0.maxRotationSpeed = 10.0
    motorParams0.feedForwardGain = 18.5
    motorParams0.minPWM = 23
    motorParams0.pidParameters.minOutput = -255
    motorParams0.pidParameters.maxOutput = 255
    motorParams0.pidParameters.k_p = 650.0
    motorParams0.pidParameters.k_i = 240.0
    motorParams0.pidParameters.k_d = 10.0

    motorParams1 = interface.MotorAngleControllerParameters()
    motorParams1.maxRotationAcceleration = 4.0
    motorParams1.maxRotationSpeed = 10.0
    motorParams1.feedForwardGain = 18.5
    motorParams1.minPWM = 21
    motorParams1.pidParameters.minOutput = -255
    motorParams1.pidParameters.maxOutput = 255
    motorParams1.pidParameters.k_p = 650.0
    motorParams1.pidParameters.k_i = 240.0
    motorParams1.pidParameters.k_d = 10.0

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    interface.setMotorAngleControllerParameters(motors[0], motorParams0)
    interface.setMotorAngleControllerParameters(motors[1], motorParams1)
