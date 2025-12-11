import functools


class hashabledict(dict):
  def __hash__(self):
    return hash(tuple(sorted(self.items())))


@functools.cache
def countPaths(nodes: hashabledict, start: str, end: str, nodesToVisit: tuple[str]) -> int:
  if start in nodesToVisit:
    visitList = list(nodesToVisit)
    visitList.remove(start)
    nodesToVisit = tuple(visitList)

  count = 0
  for node in nodes[start]:
    if node == end:
      if len(nodesToVisit) == 0:
        count += 1
    else:
      count += countPaths(nodes, node, end, nodesToVisit)
  
  return count


nodes: dict[str, tuple[str]] = {}
for line in open("input11.txt").readlines():
  node, outputs = line.strip().split(": ")
  nodes[node] = tuple(outputs.split(" "))

print(countPaths(hashabledict(nodes), "you", "out", ()))
print(countPaths(hashabledict(nodes), "svr", "out", ("dac", "fft")))