def findInvalId(scopes: list[tuple[int, int]]) -> list[int]:
  invalidIds = []
  for scope in scopes:
    for id in range(scope[0], scope[1] + 1):
      stringId = str(id)
      if len(stringId) % 2 == 0 and stringId[:len(stringId) // 2] == stringId[len(stringId) // 2:]:
        invalidIds.append(id)

  return invalidIds


def findInvalidIdExtra(scopes: list[tuple[int, int]]) -> list[int]:
  invalidIds = []
  for scope in scopes:
    for id in range(scope[0], scope[1] + 1):
      stringId = str(id)
      idLength = len(stringId)
      for i in range(1, (idLength // 2) + 1):
        if idLength % i != 0:
          continue

        parts = [stringId[:i]]
        tab = i
        while tab + i < len(stringId) + 1:
          parts.append(stringId[tab:tab + i])
          tab += i

        allEqual = True
        for i in range(1, len(parts)):
          if parts[0] != parts[i]:
            allEqual = False
            break

        if allEqual:
          invalidIds.append(id)
          break

  return invalidIds


scopes = []
for scope in open("input.txt").readline().strip().split(","):
  start, end = scope.split("-")
  scopes.append((int(start), int(end)))

invalid = findInvalId(scopes)
print(sum(invalid))
invalid = findInvalidIdExtra(scopes)
print(sum(invalid))