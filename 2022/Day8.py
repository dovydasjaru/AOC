import numpy as np

def CheckVisibility(line: np.ndarray) -> np.ndarray:
    visibility = np.full(line.shape, 0)
    highest = -1
    for i in range(line.size):
        if line[i] > highest:
            highest = line[i]
            visibility[i] = 1

    highest = -1
    for i in range(line.size):
        if line[-(i + 1)] > highest:
            highest = line[-(i + 1)]
            visibility[-(i + 1)] = 1

    return visibility

def GetScenicScore(i: int, j: int, trees: np.ndarray) -> int:
    score = 0
    for offset in range(1, i + 1):
        score += 1
        if trees[i - offset][j] >= trees[i][j]:
            break
    
    temp = 0
    for offset in range(1, trees.shape[0] - i):
        temp += 1
        if trees[i + offset][j] >= trees[i][j]:
            break
    score *= temp

    temp = 0
    for offset in range(1, j + 1):
        temp += 1
        if trees[i][j - offset] >= trees[i][j]:
            break
    score *= temp

    temp = 0
    for offset in range(1, trees.shape[1] - j):
        temp += 1
        if trees[i][j + offset] >= trees[i][j]:
            break
    score *= temp

    return score


f = open("input.txt")
trees = []
for line in f.readlines():
    trees.append([int(x) for x in list(line.strip())])

trees = np.asarray(trees)
row_visibility = []
for line in trees:
    row_visibility.append(CheckVisibility(line))
column_visibility = []
for line in np.rot90(trees):
    column_visibility.append(CheckVisibility(line))

visibility = np.add(np.asarray(row_visibility), np.rot90(np.asarray(column_visibility), 3))
print(np.count_nonzero(visibility))

highest = 0
for i in range(1, trees.shape[0] - 1):
    for j in range(1, trees.shape[1] - 1):
        current = GetScenicScore(i, j, trees)
        if current > highest:
            highest = current

print(highest)
