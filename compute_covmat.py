input_file = 'input.txt'

with open(input_file) as file:
    N = int(file.readline())
    xs = []
    ys = []
    for i in range(0, N):
        inp = file.readline().split(' ')
        xs.append(float(inp[0]))
        ys.append(float(inp[1]))

meanX = sum(xs) / N
meanY = sum(ys) / N

p00 = sum(map(lambda x: pow(x - meanX, 2), xs)) / N
p01 = sum([x * y for x, y in zip(map(lambda x: pow(x - meanX, 2), xs), map(lambda y: pow(y - meanY, 2), ys))]) / N
p10 = p01
p11 = sum(map(lambda y: pow(y - meanY, 2), ys)) / N

print str(p00) + " " + str(p01) + "\n" + str(p10) + " " + str(p11)