motor_right = 1
motor_left = 2
motor_sensor = 3

touch_sensor_left = 4
touch_sensor_right = 5

motors = [motor_left, motor_right]#, motor_sensor]

def configureRobot(interface):
    motorParams0 = interface.MotorAngleControllerParameters()
    motorParams0.maxRotationAcceleration = 5.0
    motorParams0.maxRotationSpeed = 10.0
    motorParams0.feedForwardGain = 20.5
    motorParams0.minPWM = 25
    motorParams0.pidParameters.minOutput = -255
    motorParams0.pidParameters.maxOutput = 255
    motorParams0.pidParameters.k_p = 700.0
    motorParams0.pidParameters.k_i = 0.0
    motorParams0.pidParameters.k_d = 0.0

    motorParams1 = interface.MotorAngleControllerParameters()
    motorParams1.maxRotationAcceleration = 5.0
    motorParams1.maxRotationSpeed = 10.0
    motorParams1.feedForwardGain = 20.2
    motorParams1.minPWM = 25
    motorParams1.pidParameters.minOutput = -255
    motorParams1.pidParameters.maxOutput = 255
    motorParams1.pidParameters.k_p = 700.0
    motorParams1.pidParameters.k_i = 0.0
    motorParams1.pidParameters.k_d = 0.0
    

    #motorParams2 = interface.MotorAngleControllerParameters()
    #motorParams2.maxRotationAcceleration = 5.0
    #motorParams2.maxRotationSpeed = 10.0
    #motorParams2.feedForwardGain = 20.5
    #motorParams2.minPWM = 25
    #motorParams2.pidParameters.minOutput = -255
    #motorParams2.pidParameters.maxOutput = 255
    #motorParams2.pidParameters.k_p = 100.0
    #motorParams2.pidParameters.k_i = 0.0
    #motorParams2.pidParameters.k_d = 0.0

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])
    #interface.motorEnable(motors[2])

    interface.setMotorAngleControllerParameters(motors[0], motorParams0)
    interface.setMotorAngleControllerParameters(motors[1], motorParams1)
    #interface.setMotorAngleControllerParameters(motors[2], motorParams2)
