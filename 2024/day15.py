import copy


def PrintWarehouse(warehouse: list[list[str]], robot: tuple[int]):
    cWarehouse = copy.deepcopy(warehouse)
    for i in range(len(cWarehouse)):
        line = cWarehouse[i]
        if i == robot[0]:
            line[robot[1]] = "@"
        print("".join(line))


def ConvertDirection(direction: str) -> tuple[int]:
    match direction:
        case "v":
            return (1, 0)
        case ">":
            return (0, 1)
        case "^":
            return (-1, 0)
        case "<":
            return (0, -1)
    
    raise "Did not recognise \'" + direction + "\' when converting direction"


def Travel(warehouse: list[list[int]], robot: tuple[int], directions: list[str]):
    for d in directions:
        direction = ConvertDirection(d)
        nextPosition = (robot[0] + direction[0], robot[1] + direction[1])
        if warehouse[nextPosition[0]][nextPosition[1]] == ".":
            robot = nextPosition
            continue

        if warehouse[nextPosition[0]][nextPosition[1]] == "#":
            continue
        
        lineEnd = nextPosition
        while warehouse[lineEnd[0]][lineEnd[1]] == "O":
            lineEnd = (lineEnd[0] + direction[0], lineEnd[1] + direction[1])
        
        if warehouse[lineEnd[0]][lineEnd[1]] == ".":
            warehouse[lineEnd[0]][lineEnd[1]] = "O"
            warehouse[nextPosition[0]][nextPosition[1]] = "."
            robot = nextPosition


def SumGPS(warehouse: list[list[str]]) -> int:
    sumOfGPS = 0
    for i in range(1, len(warehouse) - 1):
        for j in range(1, len(warehouse[i]) - 1):
            if warehouse[i][j] == "O":
                sumOfGPS += i * 100 + j
    
    return sumOfGPS


def DoubleUp(warehouse: list[list[str]]) -> list[list[str]]:
    doubled: list[list[str]] = []
    for i in range(len(warehouse)):
        doubled.append([])
        for j in range(len(warehouse[i])):
            match warehouse[i][j]:
                case "#":
                    doubled[i].extend(["#", "#"])
                case ".":
                    doubled[i].extend([".", "."])
                case "O":
                    doubled[i].extend(["[", "]"])
    
    return doubled

def GetMovableBoxes(warehouse, robot, direction) -> list[tuple[int, str]]:
    boxes: list[tuple[int]] = []
    if direction[0] == 0:
        lineEnd = (robot[0], robot[1] + direction[1])
        while warehouse[lineEnd[0]][lineEnd[1]] in ["[", "]"]:
            boxes.append((lineEnd[0], lineEnd[1], warehouse[lineEnd[0]][lineEnd[1]]))
            lineEnd = (lineEnd[0], lineEnd[1] + direction[1])

        if warehouse[lineEnd[0]][lineEnd[1]] == "#":
            return []
        return boxes
    
    positionsToCheck: list[tuple[int]] = [(robot[0] + direction[0], robot[1])]
    checkedPositions: list[tuple[int]] = []
    while len(positionsToCheck) > 0:
        check = positionsToCheck.pop(0)
        if warehouse[check[0] + direction[0]][check[1]] == "#":
            return []

        if warehouse[check[0]][check[1]] == "[" and (check[0], check[1] + 1) not in checkedPositions:
            positionsToCheck.append((check[0], check[1] + 1))
        elif warehouse[check[0]][check[1]] == "]" and (check[0], check[1] - 1) not in checkedPositions:
            positionsToCheck.append((check[0], check[1] - 1))
        
        if warehouse[check[0] + direction[0]][check[1]] in ["[", "]"]:
            positionsToCheck.append((check[0] + direction[0], check[1]))
        
        boxes.append((check[0], check[1], warehouse[check[0]][check[1]]))
        checkedPositions.append(check)

    return boxes
    

def DoubleTravel(warehouse: list[list[str]], robot: tuple[int], directions: list[str]):
    for d in directions:
        direction = ConvertDirection(d)
        nextPosition = (robot[0] + direction[0], robot[1] + direction[1])
        if warehouse[nextPosition[0]][nextPosition[1]] == ".":
            robot = nextPosition
            continue

        if warehouse[nextPosition[0]][nextPosition[1]] == "#":
            continue
        
        boxes = GetMovableBoxes(warehouse, robot, direction)
        if len(boxes) > 0:
            for box in boxes:
                warehouse[box[0]][box[1]] = "."
            for box in boxes:
                warehouse[box[0] + direction[0]][box[1] + direction[1]] = box[2]
            robot = nextPosition


def DoubleSumGPS(warehouse: list[list[str]]) -> int:
    sumOfGPS = 0
    for i in range(1, len(warehouse) - 1):
        for j in range(1, len(warehouse[i]) - 1):
            if warehouse[i][j] == "[":
                sumOfGPS += i * 100 + j
    
    return sumOfGPS


input = open("input15.txt").readlines()
i = 0
warehouse: list[list[str]] = []
while input[i] != "\n":
    warehouse.append(list(input[i].strip()))
    i += 1
i += 1
directions: list[str] = []
while i < len(input):
    directions.extend(list(input[i].strip()))
    i += 1
robot: tuple[int] = (0, 0)
for i in range(len(warehouse)):
    for j in range(len(warehouse[i])):
        if warehouse[i][j] == "@":
            robot = (i, j)
            warehouse[i][j] = "."

oWarehouse = copy.deepcopy(warehouse)
Travel(warehouse, robot, directions)
print(SumGPS(warehouse))

warehouse = DoubleUp(oWarehouse)
robot = (robot[0], robot[1] * 2)
DoubleTravel(warehouse, robot, directions)
print(DoubleSumGPS(warehouse))