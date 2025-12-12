import math


shapes = []

file = open("input12.txt")
line = file.readline()
while "x" not in line:
  line = file.readline()
  size = 0
  while line != "\n":
    size += line.count("#")
    line = file.readline()
  
  shapes.append(size)
  line = file.readline()

answer = 0
while line != "":
  line = line.strip()
  regionSize, shapeCounts = line.split(": ")
  regionSize = math.prod(map(int, regionSize.split("x")))
  shapeSize = 0
  shapeCounts = list(map(int, shapeCounts.split(" ")))
  for i in range(len(shapeCounts)):
    shapeSize += shapeCounts[i] * shapes[i]
  
  if shapeSize <= regionSize:
    answer += 1

  line = file.readline()

print(answer)