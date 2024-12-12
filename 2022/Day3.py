def GetError(compartment1: str, compartment2: str) -> str:
    for item in compartment1:
        if item in compartment2:
            return item
    
    raise Exception("Failed to find error")

def GetBadge(pack1: str, pack2: str, pack3: str) -> str:
    for item in pack1:
        if item in pack2 and item in pack3:
            return item
    
    raise Exception("Failed to find bagde")

def ConvertItemToNumber(error: str) -> int:
    number = ord(error)
    if number > 93:
        return number - 96
    else:
        return number - 38

f = open("input.txt")

packs = []
for line in f.readlines():
    packs.append(line.strip())

total = 0
for i in range(0, len(packs), 3):
    err = GetBadge(packs[i], packs[i + 1], packs[i + 2])
    total += ConvertItemToNumber(err)

print(total)
