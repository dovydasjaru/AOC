from sortedcontainers import SortedSet


def calculateArea(point1: tuple[int], point2: tuple[int]) -> int:
  return (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)


def findBiggestArea(tiles: list[tuple[int]]) -> int:
  biggestArea = 0
  for i in range(len(tiles)):
    for j in range(i + 1, len(tiles)):
      area = calculateArea(tiles[i], tiles[j])
      if biggestArea < area:
        biggestArea = area

  return biggestArea


def compressTiles(tiles: list[tuple[int]]) -> tuple[list[tuple[int]], tuple[SortedSet[int]]]:
  x = SortedSet(tile[0] for tile in tiles)
  y = SortedSet(tile[1] for tile in tiles)

  compressed: list[tuple[int]] = [(x.index(tile[0]), y.index(tile[1])) for tile in tiles]

  return compressed, (x, y)


def drawLine(point1: tuple[int], point2: tuple[int], tileMap: list[list[bool]]):
  if point1[0] == point2[0]:
    smaller = point1[1]
    bigger = point2[1]
    if point1[1] > point2[1]:
      smaller = point2[1]
      bigger = point1[1]

    for j in range(smaller, bigger + 1):
      tileMap[point1[0]][j] = True
  else:
    smaller = point1[0]
    bigger = point2[0]
    if point1[0] > point2[0]:
      smaller = point2[0]
      bigger = point1[0]

    for j in range(smaller, bigger + 1):
      tileMap[j][point1[1]] = True


def buildLineMap(tiles: list[tuple[int]]) -> list[list[bool]]:
  maxX = 0
  maxY = 0
  for tile in tiles:
    if tile[0] > maxX:
      maxX = tile[0]
    if tile[1] > maxY:
      maxY = tile[1]
    
  lineMap = [[False for _ in range(maxY + 1)] for _ in range(maxX + 1)]

  for i in range(len(tiles) - 1):
    drawLine(tiles[i], tiles[i + 1], lineMap)
  drawLine(tiles[0], tiles[-1], lineMap)

  return lineMap


def findBiggestAreaTiles(tiles: list[tuple[int]], tileMap: list[list[bool]]) -> list[tuple[int]]:
  tile1 = None
  tile2 = None
  area = 0
  for i in range(len(tiles)):
    for j in range(i + 1, len(tiles)):
      currentArea = calculateArea(tiles[i], tiles[j])
      if currentArea > area:
        x = [tiles[i][0], tiles[j][0]]
        y = [tiles[i][1], tiles[j][1]]
        maxPoint = (max(x), max(y))
        minPoint = (min(x), min(y))
        containsLine = False
        for ii in range(minPoint[0] + 1, maxPoint[0]):
          for jj in range(minPoint[1] + 1, maxPoint[1]):
            if tileMap[ii][jj]:
              containsLine = True
              break
        
        if not containsLine:
          tile1 = tiles[i]
          tile2 = tiles[j]
          area = currentArea

  return [tile1, tile2]



tiles = [tuple(int(number) for number in line.strip().split(",")) for line in open("input9.txt").readlines()]

print(findBiggestArea(tiles))

compressed, decompression = compressTiles(tiles)
lineMap = buildLineMap(compressed)
tile1, tile2 = findBiggestAreaTiles(compressed, lineMap)
tile1 = (decompression[0][tile1[0]], decompression[1][tile1[1]])
tile2 = (decompression[0][tile2[0]], decompression[1][tile2[1]])
print(calculateArea(tile1, tile2))