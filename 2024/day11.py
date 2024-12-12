import math


def blink(stones: list[int]) -> list[int]:
    newStones: list[int] = []
    for i in range(len(stones)):
        if stones[i] == 0:
            newStones.append(1)
            continue
        
        digitCount = int(math.log10(stones[i]) + 1)
        if digitCount % 2 == 0:
            newStones.append(int(stones[i] // (10 ** (digitCount / 2))))
            newStones.append(int(stones[i] % (10 ** (digitCount / 2))))
            continue

        newStones.append(stones[i] * 2024)

    return newStones

def countStones(stones: list[int]) -> dict[int, int]:
    stoneCount = {}
    for stone in stones:
        if stoneCount.get(stone, None) != None:
            stoneCount[stone] += 1
        else:
            stoneCount[stone] = 1

    return stoneCount



stones: list[int] = list(map(int, open("input11.txt").readline().strip().split(" ")))

for _ in range(25):
    stones = blink(stones)

print(len(stones))
stoneCount = countStones(stones)

print("first 25 unique count: " + str(len(stoneCount)))

newStoneCount: dict[int, int] = {}
for (stone, count) in stoneCount.items():
    stones = [stone]
    for _ in range(25):
        stones = blink(stones)
    
    tempStoneCount = countStones(stones)
    for (s, c) in tempStoneCount.items():
        if newStoneCount.get(s, None) != None:
            newStoneCount[s] += c * count
        else:
            newStoneCount[s] = c * count
stoneCount = newStoneCount

print("second 25 unique count: " + str(len(stoneCount)))

newStoneCount: dict[int, int] = {}
for (stone, count) in stoneCount.items():
    stones = [stone]
    for _ in range(25):
        stones = blink(stones)
    
    tempStoneCount = countStones(stones)
    for (s, c) in tempStoneCount.items():
        if newStoneCount.get(s, None) != None:
            newStoneCount[s] += c * count
        else:
            newStoneCount[s] = c * count
stoneCount = newStoneCount

print(sum(list(stoneCount.values())))