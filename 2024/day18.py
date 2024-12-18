import copy


MEMORY_SIZE = 71


class Node:
    def __init__(self, position: tuple[int], scoreToEnd: int, scoreFromStart: int):
        self.position = position
        self.scoreToEnd = scoreToEnd
        self.scoreFromStart = scoreFromStart


def CreateMemorySpace(fillValue = True) -> list[list[bool]]:
    space = []
    for _ in range(MEMORY_SIZE):
        space.append([fillValue] * MEMORY_SIZE)
    
    return space


def Simulate(memory: list[list[bool]], fallingBytes: list[tuple[int]], amount: int):
    for _ in range(amount):
        singleByte = fallingBytes.pop(0)
        memory[singleByte[0]][singleByte[1]] = False


def GetScoreToEnd(position: tuple[int]) -> int:
    return MEMORY_SIZE * 2 - position[0] - position[1]


def DrawPath(nodeConnections: dict[tuple[int], tuple[int]], position: tuple[int]) -> list[list[bool]]:
    path = CreateMemorySpace(False)
    path[position[0]][position[1]] = True

    while nodeConnections.get(position, None) != None:
        position = nodeConnections[position]
        path[position[0]][position[1]] = True
    
    return path


def GetNeighbours(position: tuple[int], memory: list[list[bool]]) -> list[tuple[int]]:
    neighbours: list[tuple[int]] = []
    if position[0] + 1 < MEMORY_SIZE and memory[position[0] + 1][position[1]]:
        neighbours.append((position[0] + 1, position[1]))
    if position[1] + 1 < MEMORY_SIZE and memory[position[0]][position[1] + 1]:
        neighbours.append((position[0], position[1] + 1))
    if position[0] - 1 >= 0 and memory[position[0] - 1][position[1]]:
        neighbours.append((position[0] - 1, position[1]))
    if position[1] - 1 >= 0 and memory[position[0]][position[1] - 1]:
        neighbours.append((position[0], position[1] - 1))

    return neighbours


def FindShortestPath(memory: list[list[bool]]) -> list[list[bool]] | None:
    searchable: list[tuple[int]] = [(0, 0)]
    nodeConnections: dict[tuple[int], tuple[int]] = {}
    scoresFromStart: dict[tuple[int], int] = {(0, 0): 0}
    scores: dict[tuple[int], int] = {(0, 0): GetScoreToEnd((0, 0))}
    while len(searchable) > 0:
        node = searchable.pop(0)
        if node[0] == MEMORY_SIZE - 1 and node[1] == MEMORY_SIZE - 1:
            return DrawPath(nodeConnections, node)

        for neighbour in GetNeighbours(node, memory):
            neighbourScoreFromStart = scoresFromStart[node] + 1
            lastNeighbourScoreFromStart = scoresFromStart.get(neighbour, None)
            if lastNeighbourScoreFromStart == None or lastNeighbourScoreFromStart > neighbourScoreFromStart:
                nodeConnections[neighbour] = node
                scoresFromStart[neighbour] = neighbourScoreFromStart
                neighbourScore = neighbourScoreFromStart + GetScoreToEnd(neighbour)
                scores[neighbour] = neighbourScore
                try:
                    searchable.remove(neighbour)
                except ValueError:
                    foundNothing = 0
                i = 0
                while i < len(searchable) and scores[searchable[i]] < neighbourScore:
                    i += 1
                searchable.insert(i + 1, neighbour)

    return None



fallingBytes: list[tuple[int]] = []
for line in open("input18.txt").readlines():
    singleByte = list(map(int, line.strip().split(",")))
    fallingBytes.append((singleByte[1], singleByte[0]))

memory = CreateMemorySpace()
Simulate(memory, copy.deepcopy(fallingBytes), 1024)
path = FindShortestPath(memory)
count = 0
for line in path:
    for tile in line:
        if tile:
            count += 1
print(count - 1)

minimum = 0
maximum = len(fallingBytes)
while maximum - minimum > 1:
    memory = CreateMemorySpace()
    midpoint = (minimum + maximum) // 2
    Simulate(memory, copy.deepcopy(fallingBytes), midpoint)
    if FindShortestPath(memory) == None:
        maximum = midpoint
    else:
        minimum = midpoint

blockingByte = fallingBytes[maximum - 1]
print(str(blockingByte[1]) + "," + str(blockingByte[0]))