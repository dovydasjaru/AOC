def FullyContains(elf1: list, elf2: list) -> bool:
    if elf1[0] >= elf2[0] and elf1[1] <= elf2[1]:
        return True
    if elf2[0] >= elf1[0] and elf2[1] <= elf1[1]:
        return True
    return False

def PartlyContains(elf1: list, elf2: list) -> bool:
    if (elf1[0] >= elf2[0] and elf1[0] <= elf2[1]) or (elf1[1] <= elf2[1] and elf1[1] >= elf2[0]):
        return True
    return False

f = open("input.txt")
pairs = []
for line in f.readlines():
    line = line.strip()
    l = line.split(",")
    pairs.append([[int(i) for i in l[0].split("-")], [int(i) for i in l[1].split("-")]])

total = 0
for p in pairs:
    if (FullyContains(p[0], p[1])):
        total += 1
    elif(PartlyContains(p[0], p[1])):
        total += 1

print(total)