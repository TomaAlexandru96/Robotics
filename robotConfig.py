motor_right = 1
motor_left = 2
touch_sensor_left = 4
touch_sensor_right = 5

motors = [motor_left, motor_right]

def configureRobot(interface):
    motorParams0 = interface.MotorAngleControllerParameters()
    motorParams0.maxRotationAcceleration = 5.0
    motorParams0.maxRotationSpeed = 10.0
    motorParams0.feedForwardGain = 19.5
    motorParams0.minPWM = 25
    motorParams0.pidParameters.minOutput = -255
    motorParams0.pidParameters.maxOutput = 255
    motorParams0.pidParameters.k_p = 610.0
    motorParams0.pidParameters.k_i = 280.0
    motorParams0.pidParameters.k_d = 10.0

    motorParams1 = interface.MotorAngleControllerParameters()
    motorParams1.maxRotationAcceleration = 5.0
    motorParams1.maxRotationSpeed = 10.0
    motorParams1.feedForwardGain = 20.5
    motorParams1.minPWM = 25
    motorParams1.pidParameters.minOutput = -255
    motorParams1.pidParameters.maxOutput = 255
    motorParams1.pidParameters.k_p = 610.0
    motorParams1.pidParameters.k_i = 280.0
    motorParams1.pidParameters.k_d = 10.0
    
    print("11")

    interface.motorEnable(motors[0])
    print("22")

    interface.motorEnable(motors[1])
    print("33")

    interface.setMotorAngleControllerParameters(motors[0], motorParams0)
    interface.setMotorAngleControllerParameters(motors[1], motorParams1)
