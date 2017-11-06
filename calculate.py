coords = []

for i in range(10):
  pairString = input("Enter {}th pair ".format(i))
  coords.append((float(pairString[0]), float(pairString[1])))
  print(coords)

xBar = sum([x for (x, y) in coords]) / 10
yBar = sum([y for (x, y) in coords]) / 10

topLeft = sum([ (x - xBar) * (x - xBar) for (x, y) in coords]) / 10
bottomRight = sum([ (y - yBar) * (y - yBar) for (x, y) in coords]) / 10

topRight = sum([(x - xBar) * (y - yBar) for (x, y) in coords]) / 10
bottomLeft = sum([(y - yBar) * (x - xBar) for (x, y) in coords]) / 10

print(xBar)
print(yBar)
print("{}, {}".format(topLeft, topRight))
print("{}, {}".format(bottomLeft, bottomRight))

