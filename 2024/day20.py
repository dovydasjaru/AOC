CARDINAL_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def GetRacePath(raceTrack: list[list[str]], start: tuple[int], end: tuple[int]) -> tuple[list[tuple[int]], list[list[int, None]]]:
    racePath: list[tuple[int]] = [start]
    weightedTrack: list[list[int, None]] = []
    for line in raceTrack:
        weightedTrack.append([None] * len(line))
    
    trackLength = 0
    weightedTrack[start[0]][start[1]] = 0
    previousPosition = (-1, -1)
    position = start
    while position != end:
        trackLength += 1
        for direction in CARDINAL_DIRECTIONS:
            possibleNextPosition = (position[0] + direction[0], position[1] + direction[1])
            if raceTrack[possibleNextPosition[0]][possibleNextPosition[1]] == "." and possibleNextPosition != previousPosition:
                racePath.append(possibleNextPosition)
                weightedTrack[possibleNextPosition[0]][possibleNextPosition[1]] = trackLength
                previousPosition = position
                position = possibleNextPosition
                break
        
    return (racePath, weightedTrack)


def CheatAmount(weightedTrack: list[list[int, None]], start: tuple[int], end: tuple[int], cheatLength) -> int | None:
    distance = abs(end[0] - start[0]) + abs(end[1] - start[1])
    if distance > cheatLength:
        return None
    
    
    difference = weightedTrack[end[0]][end[1]] - weightedTrack[start[0]][start[1]] - distance
    if difference <= 0:
        return None
    
    return difference


def CountCheats(weightedTrack: list[list[int, None]], racePath: list[tuple[int]], cheatLength: int) -> dict[int, int]:
    cheats: dict[int, int] = {}
    for i in range(0, len(racePath) - 1):
        j = i + 1
        while j < len(racePath):
            cheat = CheatAmount(weightedTrack, racePath[i], racePath[j], cheatLength)
            if cheat != None:
                if cheats.get(cheat, None) == None:
                    cheats[cheat] = 1
                else:
                    cheats[cheat] += 1
            else:
                distance = abs(racePath[i][0] - racePath[j][0]) + abs(racePath[i][1] - racePath[j][1])
                if distance > cheatLength:
                    j += distance - cheatLength - 1
            
            j += 1

    return cheats


raceTrack: list[list[str]] = []
for line in open("input20.txt").readlines():
    raceTrack.append(list(line.strip()))
start = ()
end = ()
for i in range(len(raceTrack)):
    for j in range(len(raceTrack[i])):
        match raceTrack[i][j]:
            case "S":
                raceTrack[i][j] = "."
                start = (i, j)
            case "E":
                raceTrack[i][j] = "."
                end = (i, j)

(racePath, weightedTrack) = GetRacePath(raceTrack, start, end)
cheats = CountCheats(weightedTrack, racePath, 2)

cheatsAtLeast100 = 0
for (saved, count) in cheats.items():
    if saved >= 100:
        cheatsAtLeast100 += count

print(cheatsAtLeast100)

cheats = CountCheats(weightedTrack, racePath, 20)

cheatsAtLeast100 = 0
for (saved, count) in cheats.items():
    if saved >= 100:
        cheatsAtLeast100 += count

print(cheatsAtLeast100)