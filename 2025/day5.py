def combineScopes(scopes: list[tuple[int]]) -> list[tuple[int]]:
  combined = []
  i = 0
  while i < len(scopes):
    wasCombined = False
    j = i + 1
    while j < len(scopes):
      if scopes[i][0] >= scopes[j][0] and scopes[i][1] <= scopes[j][1]:
        scopes.pop(i)
        i -= 1
        wasCombined = True
        break
      elif scopes[j][0] >= scopes[i][0] and scopes[j][1] <= scopes[i][1]:
        scopes.pop(j)
        j -= 1
      elif scopes[i][0] >= scopes[j][0] and scopes[i][0] <= scopes[j][1]:
        scopes.append((scopes[j][0], scopes[i][1]))
        scopes.pop(j)
        j -= 1
      elif scopes[i][1] >= scopes[j][0] and scopes[i][1] <= scopes[j][1]:
        scopes.append((scopes[i][0], scopes[j][1]))
        scopes.pop(j)
        j -= 1

      j += 1

    if not wasCombined:
      combined.append(scopes[i])
    
    i += 1
  
  return combined


def countFresh(scopes: list[tuple[int]], products: list[int]) -> int:
  freshProducts = 0
  for product in products:
    for scope in scopes:
      if product >= scope[0] and product <= scope[1]:
        freshProducts += 1
        break

  return freshProducts


def countAllFresh(scopes: list[tuple[int]]) -> int:
  fresh = 0
  for scope in scopes:
    fresh += scope[1] - scope[0] + 1

  return fresh


file = open("input5.txt")
line = file.readline()

scopes = []
while line != "\n":
  scopes.append(tuple(int(number) for number in line.strip().split("-")))
  line = file.readline()

line = file.readline()

products = []
while line != "":
  products.append(int(line.strip()))
  line = file.readline()

scopes = combineScopes(scopes)
print(countFresh(scopes, products))
print(countAllFresh(scopes))