def countRolls(grid: list[list[bool]], coordinate: tuple[int]) -> int:
  rolls = 0
  coordinatesToCheck = [
    (coordinate[0] - 1, coordinate[1] - 1),
    (coordinate[0], coordinate[1] - 1),
    (coordinate[0] + 1, coordinate[1] - 1),
    (coordinate[0] - 1, coordinate[1]),
    (coordinate[0] + 1, coordinate[1]),
    (coordinate[0] - 1, coordinate[1] + 1),
    (coordinate[0], coordinate[1] + 1),
    (coordinate[0] + 1, coordinate[1] + 1)
  ]
  coordinatesToCheck = filter(lambda coord: coord[0] >= 0 and coord[0] < len(grid) and coord[1] >= 0 and coord[1] < len(grid[0]), coordinatesToCheck)
  for coord in coordinatesToCheck:
    if grid[coord[0]][coord[1]]:
      rolls += 1

  return rolls


def findAccessibleCount(grid: list[list[bool]]) -> int:
  accessible = 0
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] and countRolls(grid, (i, j)) <= 3:
        accessible += 1

  return accessible


def removeAccessibleCount(grid: list[list[bool]]) -> int:
  accessible = 0
  removed = True
  while removed:
    removed = False

    for i in range(len(grid)):
      for j in range(len(grid[i])):
        if grid[i][j] and countRolls(grid, (i, j)) <= 3:
          accessible += 1
          grid[i][j] = False
          removed = True

  return accessible


grid = [[True if symbol == "@" else False for symbol in line.strip()] for line in open("input4.txt")]
print(findAccessibleCount(grid))
print(removeAccessibleCount(grid))
