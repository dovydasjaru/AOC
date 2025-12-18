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


tiles = [tuple(int(number) for number in line.strip().split(",")) for line in open("input9.txt").readlines()]

print(findBiggestArea(tiles))