import copy


CARDINAL_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def printBulkGarden(position, checkingDirection, garden):
    symbol = '.'
    if checkingDirection[0] == 0:
        if checkingDirection[1] == 1:
            symbol = '>'
        else:
            symbol = '<'
    else:
        if checkingDirection[0] == 1:
            symbol = 'v'
        else:
            symbol ='^'
    
    gardenCopy = copy.deepcopy(garden)
    gardenCopy[position[0]][position[1]] = symbol
    for line in gardenCopy:
        print(''.join(line))


def isPositionValid(position: tuple[int], grid: list[list]) -> bool:
    return position[0] >= 0 and position[1] >= 0 and position[0] < len(grid) and position[1] < len(grid[0])


def getPrice(garden: list[list[str, None]], start: tuple[int], checkedGarden: list[list[bool]]) -> int:
    area = 0
    perimeter = 0
    toCheck: list[tuple[int]] = [start]
    checkedGarden[start[0]][start[1]] = True
    while len(toCheck) > 0:
        area += 1
        position = toCheck.pop()
        for direction in CARDINAL_DIRECTIONS:
            newPosition = (position[0] + direction[0], position[1] + direction[1])
            if isPositionValid(newPosition, garden):
                if garden[position[0]][position[1]] != garden[newPosition[0]][newPosition[1]]:
                    perimeter += 1
                elif not checkedGarden[newPosition[0]][newPosition[1]]:
                    checkedGarden[newPosition[0]][newPosition[1]] = True
                    toCheck.append(newPosition)
            else:
                perimeter += 1
    
    return area * perimeter


def isNewSide(garden: list[list[str, None]], position: tuple[int], direction: tuple[int], checkedGarden: list[list[bool]]) -> bool:
    sideDirections: list[tuple[int]] = []
    if direction[0] == 0:
        sideDirections = [(1, 0), (-1, 0)]
    else:
        sideDirections = [(0, 1), (0, -1)]
    
    for sideDirection in sideDirections:
        offsetLength = 1
        neighbour = (position[0] + sideDirection[0] * offsetLength, position[1] + sideDirection[1] * offsetLength)
        while isPositionValid(neighbour, garden): # Does neighbour exist
            # Do we share a side
            if (garden[position[0]][position[1]] == garden[neighbour[0]][neighbour[1]] and 
                (not isPositionValid((neighbour[0] + direction[0], neighbour[1] + direction[1]), garden) or garden[position[0]][position[1]] != garden[neighbour[0] + direction[0]][neighbour[1] + direction[1]])): # We share a side
                if checkedGarden[neighbour[0]][neighbour[1]]: # Neighbour sides were added so we don't add current position side
                    return False

            else: # We do not share a side
                break
                
            offsetLength += 1
            neighbour = (position[0] + sideDirection[0] * offsetLength, position[1] + sideDirection[1] * offsetLength)
            
    return True


def getBulkPrice(garden: list[list[str, None]], start: tuple[int], checkedGarden: list[list[bool]]) -> int:
    area = 0
    sides = 0
    toCheck: list[tuple[int]] = [start]
    walkedGarden: list[tuple[bool]] = []
    for i in range(len(garden)):
        walkedGarden.append([False] * len(garden[i]))
    checkedGarden[start[0]][start[1]] = True
    while len(toCheck) > 0:
        area += 1
        position = toCheck.pop()
        walkedGarden[position[0]][position[1]] = True
        for direction in CARDINAL_DIRECTIONS:
            newPosition = (position[0] + direction[0], position[1] + direction[1])
            if isPositionValid(newPosition, garden):
                if garden[position[0]][position[1]] != garden[newPosition[0]][newPosition[1]]:
                    if isNewSide(garden, position, direction, walkedGarden):
                        sides += 1
                elif not checkedGarden[newPosition[0]][newPosition[1]]:
                    checkedGarden[newPosition[0]][newPosition[1]] = True
                    toCheck.append(newPosition)
            elif isNewSide(garden, position, direction, walkedGarden):
                sides += 1
    
    return area * sides


garden: list[list[str, None]] = []
checkedGarden: list[list[bool]] = []
checkedGardenBulk: list[list[bool]] = []
for line in open("input12.txt").readlines():
    garden.append(list(line.strip()))
    checkedGarden.append([False] * len(garden[-1]))
    checkedGardenBulk.append([False] * len(garden[-1]))

totalPrice = 0
totalBulkPrice = 0
for i in range(len(garden)):
    for j in range(len(garden[i])):
        if not checkedGarden[i][j]:
            totalPrice += getPrice(garden, (i, j), checkedGarden)
            totalBulkPrice += getBulkPrice(garden, (i, j), checkedGardenBulk)

print(totalPrice)
print(totalBulkPrice)