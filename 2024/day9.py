import copy

def printDiskMap(diskMap: list[int, None]):
    print("".join(map(lambda x: "." if x == None else str(x) , diskMap)))


def expandDiskMap(diskMap: list[int]) -> list[int, None]:
    fileId = 0
    expandedMap: list[int, None] = []
    for i in range(0, len(diskMap) - 1, 2):
        expandedMap.extend([fileId] * diskMap[i])
        expandedMap.extend([None] * diskMap[i + 1])
        fileId += 1

    expandedMap.extend([fileId] * diskMap[-1])
    return expandedMap


def compactDiskMap(diskMap: list[int, None]) -> list[int]:
    i = 0
    while i < len(diskMap):
        if diskMap[i] != None:
            i += 1
            continue

        lastDigit = diskMap.pop()
        if lastDigit != None:
            diskMap[i] = lastDigit
            i += 1
    
    return diskMap


def findEmptyOfSize(diskMap: list[int, None], size: int, searchLimit: int) -> int | None:
    i = 0
    while i < searchLimit:
        if diskMap[i] != None:
            i += 1
            continue
        
        emptySize = 0
        j = i
        while diskMap[j] == None and j < searchLimit:
            emptySize += 1
            j += 1

        if emptySize >= size:
            return i
        
        i = j
    
    return None


def smartCompactDiskMap(diskMap: list[int, None]) -> list[int, None]:
    i = len(diskMap) - 1
    nextId = diskMap[i]
    while i >= 0:
        if diskMap[i] != nextId:
            i -= 1
            continue
        
        j = i
        while diskMap[j] == nextId:
            j -= 1
        nextId -= 1

        fileSize = i - j
        emptyIndex = findEmptyOfSize(diskMap, fileSize, i)
        if emptyIndex == None:
            i = j
            continue

        while i > j:
            diskMap[emptyIndex] = diskMap[i]
            diskMap[i] = None
            i -= 1
            emptyIndex += 1
    
    return diskMap


def calculateChecksum(diskMap: list[int, None]) -> int:
    sum = 0
    for i in range(len(diskMap)):
        if diskMap[i] != None:
            sum += i * diskMap[i]

    return sum


diskMap = list(map(int, list(open("input9.txt").readline().strip())))

expanded = expandDiskMap(diskMap)
compacted = compactDiskMap(copy.copy(expanded))
smartCompacted = smartCompactDiskMap(expanded)

print(calculateChecksum(compacted))
print(calculateChecksum(smartCompacted))