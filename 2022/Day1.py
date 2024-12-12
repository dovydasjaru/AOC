f = open("input.txt")

elfs = [0]
for line in f.readlines():
    line = line.strip()
    if line == "":
        elfs.append(0)
    else:
        elfs[-1] += int(line)

print(sum(sorted(elfs, reverse=True)[0:3]))
