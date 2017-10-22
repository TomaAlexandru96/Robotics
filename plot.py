import matplotlib.pyplot as plt
import sys

logfile = "logfile.txt"
diff = False

if len(sys.argv) > 1:
    for arg in sys.argv:
        arg = arg.split('=')
        if arg[0] == 'd':
            diff = arg[1]
        elif arg[0] == 'f':
            logfile = arg[1]

with open(logfile) as f:
    read_data = f.readlines()

time = []
reference_angle0 = []
angle0 = []
reference_angle1 = []
angle1 = []

for line in read_data:
    if len(line.split()) == 1:
        continue
    time.append(line.split()[0])
    reference_angle0.append(line.split()[1])
    angle0.append(line.split()[2])
    reference_angle1.append(line.split()[3])
    angle1.append(line.split()[4])

if not diff:
    plt.hold(True)
    plt.plot(time, reference_angle0, label="Reference Angle 0", color="green")
    plt.plot(time, angle0, label="Angle 0", color="blue")
    plt.plot(time, reference_angle1, label="Reference Angle 1", color="red")
    plt.plot(time, angle1, label="Angle 1", color="purple")
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    
    plt.title("Calibration")
    plt.xlabel("Time")
else:
    diff0 = []
    diff1 = []
    for i in range(0, len(reference_angle0)):
        diff0.append(float(reference_angle0[i]) - float(angle0[i]))
        diff1.append(float(reference_angle1[i]) - float(angle1[i]))
    plt.hold(True)
    plt.plot(time, diff0, label="Angle Diff 0", color="blue")
    plt.plot(time, diff1, label="Angle Diff 1", color="red")
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    
    plt.title("Calibration Differential")
    plt.xlabel("Time")
plt.show()
