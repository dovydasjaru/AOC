import math


def FindMeshGroups(pairs: list[tuple[str]]) -> list[set[str]]:
    connections: dict[str, set[str]] = {}
    for pair in pairs:
        if connections.get(pair[0], None) == None:
            connections[pair[0]] = set()
        if connections.get(pair[1], None) == None:
            connections[pair[1]] = set()
        
        connections[pair[0]].add(pair[1])
        connections[pair[1]].add(pair[0])
    
    groups: list[set[str]] = []
    for pair in pairs:
        groups.append(set(pair))
    
    for pc, connected in connections.items():
        for group in groups:
            if connected.issuperset(group):
                group.add(pc)

    i = 0
    while(i < len(groups)):
        j = i + 1
        while j < len(groups):
            if groups[i].issubset(groups[j]):
                groups.pop(j)
                j -= 1
            j += 1
        i += 1
    
    return groups


def FindGroupsPCStartingWith(groups: list[set[str]], match: str) -> list[set[str]]:
    matched: list[set[str]] = []
    for group in groups:
        for pc in group:
            if match == pc[0]:
                matched.append(set(group))
                break
    
    return matched


def GetCombinbinationCount(objectsCount: int, choosingCount: int) -> int:
    return math.factorial(objectsCount) / (math.factorial(choosingCount) * math.factorial(objectsCount - choosingCount))


pairs: list[tuple[str]] = []
for line in open("input23.txt").readlines():
    pair = line.strip().split("-")
    pairs.append(tuple(pair))

groups = FindMeshGroups(pairs)

groupsWithT = FindGroupsPCStartingWith(groups, "t")
groupsWithT = filter(lambda x: len(x) > 2, groupsWithT)
answer = 0
uniqueThreeGroups = set()
for group in groupsWithT:
    group = list(group)
    index = 0
    while index < len(group):
        if group[index][0] != "t":
            index += 1
            continue
    
        pc = group.pop(index)
        for i in range(len(group) - 1):
            for j in range(i + 1, len(group)):
                newGroup = [pc, group[j], group[i]]
                newGroup.sort()
                uniqueThreeGroups.add(tuple(newGroup))

print(len(uniqueThreeGroups))

largest = groups[0]
for i in range(1, len(groups)):
    if len(groups[i]) > len(largest):
        largest = groups[i]

largest = list(largest)
largest.sort()
print(",".join(largest))