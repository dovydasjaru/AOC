import copy
import json
import functools


NUMERIC_KEYPAD = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2)
}
DIRECTIONAL_KEYPAD = {
    "A": (0, 2),
    "^": (0, 1),
    ">": (1, 2),
    "v": (1, 1),
    "<": (1, 0)
}
NUMERIC_EXCEPTIONS = [(0, 0), (1, 0), (2, 0), (3, 1), (3, 2)]
DIRECTIONAL_EXCEPTIONS = [(0, 1), (0, 2), (1, 0)]


def GetTravelPosibilities(start: tuple[int], end: tuple[int]) -> list[str]:
    posibilities: list[str] = []
    difference = (end[0] - start[0], end[1] - start[1])
    command = ""
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    command += "A"
    posibilities.append(command)

    if difference[0] == 0 or difference[1] == 0:
        return posibilities
    
    command = ""
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[0] > 0:
        command += "v" * difference[0]
    command += "A"
    if command != posibilities[0]:
        posibilities.append(command)
    
    if end in NUMERIC_EXCEPTIONS and start in NUMERIC_EXCEPTIONS:
        return posibilities
    
    command = ""
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[1] > 0:
        command += ">" * difference[1]
    command += "A"
    if command not in posibilities:
        posibilities.append(command)

    command = ""
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    command += "A"
    if command not in posibilities:
        posibilities.append(command)

    return posibilities


def GetRobotTravelPosibilities(start: tuple[int], end: tuple[int]) -> list[str]:
    posibilities: list[str] = []
    difference = (end[0] - start[0], end[1] - start[1])
    command = ""
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    command += "A"
    posibilities.append(command)

    if difference[0] == 0 or difference[1] == 0:
        return posibilities
    
    command = ""
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    command += "A"
    if command != posibilities[0]:
        posibilities.append(command)
    
    if end in DIRECTIONAL_EXCEPTIONS and start in DIRECTIONAL_EXCEPTIONS:
        return posibilities
    
    command = ""
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[1] > 0:
        command += ">" * difference[1]
    if difference[0] > 0:
        command += "v" * difference[0]
    command += "A"
    if command not in posibilities:
        posibilities.append(command)

    command = ""
    if difference[1] < 0:
        command += "<" * (difference[1] * -1)
    if difference[0] < 0:
        command += "^" * (difference[0] * -1)
    if difference[0] > 0:
        command += "v" * difference[0]
    if difference[1] > 0:
        command += ">" * difference[1]
    command += "A"
    if command not in posibilities:
        posibilities.append(command)

    return posibilities


def Dictionarise(code: str) -> dict[str, int]:
    subCodes: dict[str, int] = {}
    for sub in code.split("A")[:-1]:
        if subCodes.get(sub + "A", None) == None:
            subCodes[sub + "A"] = 1
        else:
            subCodes[sub + "A"] += 1

    return subCodes


def CalculateCodeLength(code: dict[str, int]) -> int:
    length = 0
    for (part, partCount) in code.items():
        length += len(part) * partCount
    
    return length


def GetMinimumRobotControlCode(listCodeParts: list[dict[str, int]], count: int) -> int:
    newListCodeParts = []
    for codeParts in listCodeParts:
        if count == 0:
            return CalculateCodeLength(codeParts)
        
        nextCodes: list[dict[str, int]] = [{}]
        position = DIRECTIONAL_KEYPAD["A"]
        for (code, codeCount) in codeParts.items():
            for char in code:
                nextPosition = DIRECTIONAL_KEYPAD[char]
                posibilities = GetRobotTravelPosibilities(position, nextPosition)
                
                oNextCodes = copy.deepcopy(nextCodes)
                for _ in range(1, len(posibilities)):
                    nextCodes.extend(copy.deepcopy(oNextCodes))

                for i in range(len(nextCodes) // len(posibilities)):
                    for j in range(len(posibilities)):
                        if nextCodes[i * len(posibilities) + j].get(posibilities[j], None) == None:
                            nextCodes[i * len(posibilities) + j][posibilities[j]] = codeCount
                        else:
                            nextCodes[i * len(posibilities) + j][posibilities[j]] += codeCount
                
                position = nextPosition

        jsonCodes = set()
        for nextCode in nextCodes:
            jsonCodes.add(json.dumps(nextCode, sort_keys=True))
        for jsonCode in jsonCodes:
            newListCodeParts.append(json.loads(jsonCode))
    
    minimum = None
    shortestCodes = []
    for newCodeParts in newListCodeParts:
        currentMinimum = CalculateCodeLength(newCodeParts)
        if minimum == None or currentMinimum < minimum:
            shortestCodes = [newCodeParts]
            minimum = currentMinimum
        elif minimum == currentMinimum:
            shortestCodes.append(newCodeParts)
    
    newListCodeParts = shortestCodes
    
    return GetMinimumRobotControlCode(newListCodeParts, count - 1)


def GetMinimumLength(code: str, numberOfRobots: int) -> int:
    minimum = None
    position = NUMERIC_KEYPAD["A"]
    paths: list[str] = [""]
    for char in code:
        nextPosition = NUMERIC_KEYPAD[char]
        posibilities = GetTravelPosibilities(position, nextPosition)

        oPaths = copy.deepcopy(paths)
        for _ in range(1, len(posibilities)):
            paths.extend(copy.deepcopy(oPaths))

        for i in range(len(paths) // len(posibilities)):
            for j in range(len(posibilities)):
                paths[i * len(posibilities) + j] += posibilities[j]
        
        position = nextPosition

    for path in paths:
        dictPath = Dictionarise(path)
        currentMinimum = GetMinimumRobotControlCode([dictPath], numberOfRobots - 1)
        if minimum == None or minimum > currentMinimum:
            minimum = currentMinimum
            
    return minimum


input = open("input21.txt").readlines()
codes = list(map(lambda x: x.strip(), input))

ans1 = 0
ans2 = 0
for code in codes:
    length = GetMinimumLength(code, 3)
    ans1 += length * int(code[:-1])
    length = GetMinimumLength(code, 26)
    ans2 += length * int(code[:-1])

print(ans1)
print(ans2)