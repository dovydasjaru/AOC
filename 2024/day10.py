import copy

def printMap(topoMap: list[list[int, None]]):
    for line in topoMap:
        print("".join(list(map(lambda x: "." if x == None else str(x), line))))


def countTrails(topoMap: list[list[int, None]], position: tuple[int]) -> int:
    currentHeight = topoMap[position[0]][position[1]]
    topoMap[position[0]][position[1]] = None
    if currentHeight == 9:
        return 1
    
    count = 0
    if position[0] + 1 < len(topoMap) and topoMap[position[0] + 1][position[1]] == currentHeight + 1:
        count += countTrails(topoMap, (position[0] + 1, position[1]))
    if position[0] - 1 >= 0 and topoMap[position[0] - 1][position[1]] == currentHeight + 1:
        count += countTrails(topoMap, (position[0] - 1, position[1]))
    if position[1] + 1 < len(topoMap[0]) and topoMap[position[0]][position[1] + 1] == currentHeight + 1:
        count += countTrails(topoMap, (position[0], position[1] + 1))
    if position[1] - 1 >= 0 and topoMap[position[0]][position[1] - 1] == currentHeight + 1:
        count += countTrails(topoMap, (position[0], position[1] - 1))
    
    return count


def countDistinctTrails(topoMap: list[list[int]], position: tuple[int]) -> int:
    currentHeight = topoMap[position[0]][position[1]]
    if currentHeight == 9:
        return 1
    
    count = 0
    if position[0] + 1 < len(topoMap) and topoMap[position[0] + 1][position[1]] == currentHeight + 1:
        count += countDistinctTrails(topoMap, (position[0] + 1, position[1]))
    if position[0] - 1 >= 0 and topoMap[position[0] - 1][position[1]] == currentHeight + 1:
        count += countDistinctTrails(topoMap, (position[0] - 1, position[1]))
    if position[1] + 1 < len(topoMap[0]) and topoMap[position[0]][position[1] + 1] == currentHeight + 1:
        count += countDistinctTrails(topoMap, (position[0], position[1] + 1))
    if position[1] - 1 >= 0 and topoMap[position[0]][position[1] - 1] == currentHeight + 1:
        count += countDistinctTrails(topoMap, (position[0], position[1] - 1))
    
    return count
    

topoMap: list[list[int]] = []
for line in open("input10.txt").readlines():
    topoMap.append(list(map(int, list(line.strip()))))

trailCount = 0
distinctTrailCount = 0
for i in range(len(topoMap)):
    for j in range(len(topoMap[i])):
        if topoMap[i][j] == 0:
            trailCount += countTrails(copy.deepcopy(topoMap), (i, j))
            distinctTrailCount += countDistinctTrails(copy.deepcopy(topoMap), (i, j))

print(trailCount)
print(distinctTrailCount)