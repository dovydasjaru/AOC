from pprint import pprint
import copy

def isInBound(stationMap: list[list[str]], antinode: tuple[int]) -> bool:
    return antinode[0] >= 0 and antinode[1] >= 0 and antinode[0] < len(stationMap) and antinode[1] < len(stationMap[0])


def canAntinode(stationMap: list[list[str]], antinode: tuple[int]) -> bool:
    return isInBound(stationMap, antinode) and stationMap[antinode[0]][antinode[1]] != "#"


originalStationMap: list[list[str]] = []
for line in open("input8.txt").readlines():
    originalStationMap.append(list(line.strip()))

stationLocations: dict[str, list[tuple[int]]] = {}
for i in range(len(originalStationMap)):
    for j in range(len(originalStationMap[i])):
        if originalStationMap[i][j] != ".":
            if stationLocations.get(originalStationMap[i][j], None) == None:
                stationLocations[originalStationMap[i][j]] = []
            stationLocations[originalStationMap[i][j]].append((i, j))

antinodeCount = 0
stationMap = copy.deepcopy(originalStationMap)
for locations in stationLocations.values():
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            difference = (locations[j][0] - locations[i][0], locations[j][1] - locations[i][1])
            antinode = (locations[j][0] + difference[0], locations[j][1] + difference[1])
            if canAntinode(stationMap, antinode):
                antinodeCount += 1
                stationMap[antinode[0]][antinode[1]] = "#"
            antinode = (locations[i][0] - difference[0], locations[i][1] - difference[1])
            if canAntinode(stationMap, antinode):
                antinodeCount += 1
                stationMap[antinode[0]][antinode[1]] = "#"

print(antinodeCount)

antinodeCount = 0
stationMap = copy.deepcopy(originalStationMap)
for locations in stationLocations.values():
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            difference = (locations[j][0] - locations[i][0], locations[j][1] - locations[i][1])
            antinode = (locations[j][0] + difference[0], locations[j][1] + difference[1])
            while isInBound(stationMap, antinode):
                if stationMap[antinode[0]][antinode[1]] != "#":
                    antinodeCount += 1
                    stationMap[antinode[0]][antinode[1]] = "#"
                antinode = (antinode[0] + difference[0], antinode[1] + difference[1])
            
            antinode = (locations[i][0] - difference[0], locations[i][1] - difference[1])
            while isInBound(stationMap, antinode):
                if stationMap[antinode[0]][antinode[1]] != "#":
                    antinodeCount += 1
                    stationMap[antinode[0]][antinode[1]] = "#"
                antinode = (antinode[0] - difference[0], antinode[1] - difference[1])
            
            if canAntinode(stationMap, locations[i]):
                antinodeCount += 1
                stationMap[locations[i][0]][locations[i][1]] = "#"
            if canAntinode(stationMap, locations[j]):
                antinodeCount += 1
                stationMap[locations[j][0]][locations[j][1]] = "#"

print(antinodeCount)