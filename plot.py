import matplotlib.pyplot as plt

with open("logfile.txt") as f:
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

plt.hold(True)
plt.plot(time, reference_angle0, label="Reference Angle 0", color="green")
plt.plot(time, angle0, label="Angle 0", color="blue")
plt.plot(time, reference_angle1, label="Reference Angle 1", color="red")
plt.plot(time, angle1, label="Angle 1", color="purple")

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

plt.title("Calibration")
plt.xlabel("Time")

plt.show()
