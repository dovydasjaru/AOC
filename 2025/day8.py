import math
from sortedcontainers import SortedKeyList


def calculateDistance(box1: tuple[int], box2: tuple[int]) -> float:
  return math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2)


def buildSortedDistances(coordinates: list[tuple[int]]) -> SortedKeyList:
  distances: SortedKeyList = SortedKeyList(key=lambda x: x[0])
  while len(coordinates) > 0:
    box = coordinates.pop()
    for coord in coordinates:
      distances.add((calculateDistance(box, coord), box, coord)) 

  return distances


def connectByDistance(distances: SortedKeyList, connectionCount: int) -> list[set[tuple[int]]]:
  circuits: list[set[tuple[int]]] = []
  for i in range(connectionCount):
    _, box1, box2 = distances[i]

    box1Circuit = None
    box2Circuit = None
    for circuit in circuits:
      if box1 in circuit:
        box1Circuit = circuit
        circuit.add(box2)
      elif box2 in circuit:
        box2Circuit = circuit
        circuit.add(box1)
    
    if box1Circuit != None and box2Circuit != None:
      circuits.remove(box1Circuit)
      circuits.remove(box2Circuit)
      circuits.append(box1Circuit.union(box2Circuit))
    elif box1Circuit == None and box2Circuit == None:
      circuits.append(set([box1, box2]))
  
  return circuits


def  findLastConnection(distances: SortedKeyList, boxCount: int) -> tuple[tuple[int]]:
  circuits: list[set[tuple[int]]] = [set([distances[0][1], distances[0][2]])]
  lastBox1 = distances[0][1]
  lastBox2 = distances[0][2]
  i = 1
  while len(circuits[0]) < boxCount:
    _, lastBox1, lastBox2 = distances[i]

    box1Circuit = None
    box2Circuit = None
    for circuit in circuits:
      if lastBox1 in circuit:
        box1Circuit = circuit
        circuit.add(lastBox2)
      elif lastBox2 in circuit:
        box2Circuit = circuit
        circuit.add(lastBox1)
    
    if box1Circuit != None and box2Circuit != None:
      circuits.remove(box1Circuit)
      circuits.remove(box2Circuit)
      circuits.append(box1Circuit.union(box2Circuit))
    elif box1Circuit == None and box2Circuit == None:
      circuits.append(set([lastBox1, lastBox2]))

    i += 1
  
  return (lastBox1, lastBox2)


coordinates = [tuple(int(number) for number in line.strip().split(",")) for line in open("input8.txt").readlines()]
distances = buildSortedDistances(coordinates.copy())
circuits = connectByDistance(distances, 1000)
circuitSizes = list(map(len, circuits))

answer = 1
for _ in range(3):
  biggest = max(circuitSizes)
  answer *= biggest
  circuitSizes.remove(biggest)
print(answer)

box1, box2 = findLastConnection(distances, len(coordinates))
print(box1[0] * box2[0])