from pprint import pprint
import copy


def nextDirection(direction: tuple[int]) -> tuple[int]:
    if direction[0] == 1:
        return (0, -1)
    elif direction[1] == -1:
        return (-1, 0)
    elif direction[0] == -1:
        return (0, 1)
    else:
        return (1, 0)


def willLoop(mapGrid: list[list[str]], guard: list[int], direction: tuple[int, int]) -> bool:
    history = {((guard[0], guard[1]), direction)}
    while guard[0] + direction[0] >= 0 and guard[0] + direction[0] < len(mapGrid) and guard[1] + direction[1] >= 0 and guard[1] + direction[1] < len(mapGrid[0]):
        nextTile = mapGrid[guard[0] + direction[0]][guard[1] + direction[1]]
        match nextTile:
            case ".":
                guard[0] += direction[0]
                guard[1] += direction[1]
                mapGrid[guard[0]][guard[1]] = "X"
                if history.issuperset({((guard[0], guard[1]), direction)}):
                    return True
                else:
                    history.add(((guard[0], guard[1]), direction))
            case "X":
                guard[0] += direction[0]
                guard[1] += direction[1]
                if history.issuperset({((guard[0], guard[1]), direction)}):
                    return True
                else:
                    history.add(((guard[0], guard[1]), direction))
            case "#":
                direction = nextDirection(direction)

    return False

mapGrid: list[list[str]] = []
for line in open("input6.txt").readlines():
    mapGrid.append(list(line.strip()))

guard = []
for i in range(len(mapGrid)):
    try:
        j = mapGrid[i].index("^")
    except (ValueError):
        continue

    guard = [i, j]
    break

direction = (-1, 0)
visitedTiles = 1
mapGrid[guard[0]][guard[1]] = "X"
originalMap = copy.deepcopy(mapGrid)
loops = 0
while guard[0] + direction[0] >= 0 and guard[0] + direction[0] < len(mapGrid) and guard[1] + direction[1] >= 0 and guard[1] + direction[1] < len(mapGrid[0]):
    nextTile = mapGrid[guard[0] + direction[0]][guard[1] + direction[1]]
    match nextTile:
        case ".":
            visitedTiles += 1
            mapCopy = copy.deepcopy(originalMap)
            mapCopy[guard[0] + direction[0]][guard[1] + direction[1]] = "#"
            mapCopy[guard[0]][guard[1]] = "X"
            if willLoop(mapCopy, copy.copy(guard), nextDirection(direction)):
                loops += 1
            
            guard[0] += direction[0]
            guard[1] += direction[1]
            mapGrid[guard[0]][guard[1]] = "X"
        case "X":
            guard[0] += direction[0]
            guard[1] += direction[1]
        case "#":
            direction = nextDirection(direction)

print(visitedTiles)
print(loops)
