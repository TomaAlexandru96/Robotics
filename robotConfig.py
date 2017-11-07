motor_right = 3
motor_left = 1
touch_sensor_left = 4
touch_sensor_right = 5

motors = [motor_left, motor_right]

def configureRobotCarpet(interface):
    motorParams0 = interface.MotorAngleControllerParameters()
    motorParams0.maxRotationAcceleration = 4.0
    motorParams0.maxRotationSpeed = 10.0
    motorParams0.feedForwardGain = 13.17
    motorParams0.minPWM = 25
    motorParams0.pidParameters.minOutput = -255
    motorParams0.pidParameters.maxOutput = 255
    motorParams0.pidParameters.k_p = 700.0
    motorParams0.pidParameters.k_i = 135.0
    motorParams0.pidParameters.k_d = 30.0

    motorParams1 = interface.MotorAngleControllerParameters()
    motorParams1.maxRotationAcceleration = 4.0
    motorParams1.maxRotationSpeed = 10.0
    motorParams1.feedForwardGain = 13.12
    motorParams1.minPWM = 25
    motorParams1.pidParameters.minOutput = -255
    motorParams1.pidParameters.maxOutput = 255
    motorParams1.pidParameters.k_p = 700.0
    motorParams1.pidParameters.k_i = 135.0
    motorParams1.pidParameters.k_d = 30.0

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    interface.setMotorAngleControllerParameters(motors[0], motorParams0)
    interface.setMotorAngleControllerParameters(motors[1], motorParams1)

def configureRobotPaper(interface):
    motorParams0 = interface.MotorAngleControllerParameters()
    motorParams0.maxRotationAcceleration = 4.0
    motorParams0.maxRotationSpeed = 10.0
    motorParams0.feedForwardGain = 13.17
    motorParams0.minPWM = 25
    motorParams0.pidParameters.minOutput = -255
    motorParams0.pidParameters.maxOutput = 255
    motorParams0.pidParameters.k_p = 570.0
    motorParams0.pidParameters.k_i = 195.0
    motorParams0.pidParameters.k_d = 30.0

    motorParams1 = interface.MotorAngleControllerParameters()
    motorParams1.maxRotationAcceleration = 4.0
    motorParams1.maxRotationSpeed = 10.0
    motorParams1.feedForwardGain = 13.12
    motorParams1.minPWM = 25
    motorParams1.pidParameters.minOutput = -255
    motorParams1.pidParameters.maxOutput = 255
    motorParams1.pidParameters.k_p = 570.0
    motorParams1.pidParameters.k_i = 195.0
    motorParams1.pidParameters.k_d = 30.0

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    interface.setMotorAngleControllerParameters(motors[0], motorParams0)
    interface.setMotorAngleControllerParameters(motors[1], motorParams1)
