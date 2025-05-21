def isPair(lock: tuple[int], key: tuple[int]) -> bool:
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    
    return True


def CountPairs(locks: set[tuple[int]], keys: set[tuple[int]]) -> int:
    count = 0
    for lock in locks:
        for key in keys:
            if isPair(lock, key):
                count += 1
    
    return count


locks: list[tuple[int]] = []
keys: list[tuple[int]] = []

inputFile = open("input25.txt").readlines()
index = 0
while index < len(inputFile):
    heights = [None, None, None, None, None]
    if inputFile[index] == ".....\n":
        for i in range(1, 7):
            for j in range(len(heights)):
                if inputFile[index + i][j] == "#" and heights[j] == None:
                    heights[j] = 6 - i
        
        keys.append(tuple(heights))
    else:
        for i in range(1, 7):
            for j in range(len(heights)):
                if inputFile[index + i][j] == "." and heights[j] == None:
                    heights[j] = i - 1
        
        locks.append(tuple(heights))
    
    index += 8

print(CountPairs(locks, keys))