def countOnZero(list: list[int]) -> int:
  position = 50
  count = 0
  for rotation in list:
    position += rotation
    position = position % 100
    if position == 0:
      count += 1

  return count


def countThroughZero(list: list[int]) -> int:
  position = 50
  count = 0
  for rotation in list:
    initialPosition = position
    rotatedPosition = position + rotation
    position = rotatedPosition % 100

    if rotatedPosition < 0:
      count += -1 * (rotatedPosition // 100)
      if initialPosition == 0:
        count -= 1
      if position == 0:
        count += 1
    elif rotatedPosition > 0:
      count += rotatedPosition // 100
    elif rotatedPosition == 0:
      count += 1

  return count


input = []
for line in open("input1.txt").readlines():
  line = line.strip()
  line = line.replace("R", "")
  line = line.replace("L", "-")
  input.append(int(line))

print(countOnZero(input))
print(countThroughZero(input))