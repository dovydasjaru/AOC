import copy


def PrintMap(deerMap: list[list[str]], position: tuple[int], crossroads: list[list[int, None]] | None = None):
    oMap = copy.deepcopy(deerMap)
    for i in range(len(oMap)):
        line = oMap[i]
        if i == position[0]:
            line[position[1]] = "@"
        if crossroads != None:
            for j in range(len(deerMap)):
                if crossroads[i][j] != None:
                    line[j] = str(crossroads[i][j])

        print("".join(line))


def GetScoreToEnd(position: tuple[int], end: tuple[int]) -> int:
    turnIsNeeded = position[0] != end[0] and position[1] != end[1]
    return abs(end[0] -position[0]) + abs(end[1] - position[1]) + 1000 * int(turnIsNeeded)


def GetNeighbours(deerMap: list[list[str]], node: tuple[tuple[int]]) -> list[tuple[tuple[int]]]:
    position = node[0]
    direction = node[1]
    neighbours: list[tuple[tuple[int]]] = []
    if deerMap[position[0] + direction[0]][position[1] + direction[1]] != "#":
        neighbours.append(((position[0] + direction[0], position[1] + direction[1]), direction))
    sides = [(0, 1), (0, -1)]
    if direction[0] == 0:
        sides = [(1, 0), (-1, 0)]
    
    for side in sides:
        if deerMap[position[0] + side[0]][position[1] + side[1]] != "#":
            neighbours.append(((position[0] + side[0], position[1] + side[1]), side))

    return neighbours


def BuildPathsMap(previousSteps: dict[tuple[tuple[int]], tuple[tuple[int]]], ends: list[tuple[tuple[int]]], height: int, width: int) -> list[list[list[bool]]]:
    pathsMap = []
    for _ in range(height):
        pathsMap.append([False] * width)

    previous = ends
    while len(previous) > 0:
        p = previous.pop(0)
        pathsMap[p[0][0]][p[0][1]] = True
        next = previousSteps.get(p, [])
        for n in next:
            if n not in previous:
                previous.append(n)
    
    return pathsMap


def FindShortests(deerMap: list[list[str]], start: tuple[int], end: tuple[int], direction: tuple[int]) -> tuple[int, list[list[bool]]]:
    minimalScore = None
    endNeighbours = []
    checkable: list[tuple[tuple[int]]] = [(start, direction)]
    previousStep: dict[tuple[tuple[int]], list[tuple[tuple[int]]]] = {}
    scoreFromStart: dict[tuple[tuple[int]], int] = {(start, direction): 0}
    score: dict[tuple[tuple[int]], int] = {(start, direction): GetScoreToEnd(start, end)}
    while len(checkable) > 0:
        current = checkable.pop(0)
        if (current[0] == end):
            raise Exception("Something baaad")
        
        for neighbour in GetNeighbours(deerMap, current):
            tentativeScore = scoreFromStart[current] + 1 + 1000 * int(current[1] != neighbour[1])
            previousScore = scoreFromStart.get(neighbour, None)
            if previousScore == None or tentativeScore <= previousScore:
                neighbourScore = tentativeScore + GetScoreToEnd(neighbour[0], end)
                if neighbour[0] == end:
                    if  minimalScore == None or minimalScore > neighbourScore:
                        previousStep[neighbour] = [current]
                        endNeighbours = [neighbour]
                        minimalScore = neighbourScore
                    elif minimalScore != None and minimalScore == neighbourScore:
                        previousStep[neighbour].append(current)
                        endNeighbours.append(neighbour)
                    continue

                previousStepMade = previousStep.get(neighbour, None)
                if previousStepMade == None:
                    previousStep[neighbour] = [current]
                else:
                    previousStep[neighbour].append(current)
                scoreFromStart[neighbour] = tentativeScore
                score[neighbour] = neighbourScore

                try:
                    checkable.remove(neighbour)
                except:
                    doNothing = 0
                i = 0
                while i < len(checkable) and score[checkable[i]] < neighbourScore:
                    i += 1
                checkable.insert(i, neighbour)
    
    return (minimalScore, BuildPathsMap(previousStep, endNeighbours, len(deerMap), len(deerMap[0])))



deerMap: list[list[str]] = []
for line in open("input16.txt").readlines():
    deerMap.append(list(line.strip()))

start = (len(deerMap) - 2, 1)
end = (1, len(deerMap) - 2)
deerMap[start[0]][start[1]] = "."
deerMap[end[0]][end[1]] = "."
direction = (0, 1)
ans = FindShortests(copy.deepcopy(deerMap), start, end, direction)
print(ans[0])

combinedMap = ans[1]
count = 0
for i in range(len(combinedMap)):
    for j in range(len(combinedMap[i])):
        if combinedMap[i][j]:
            count += 1

print(count)