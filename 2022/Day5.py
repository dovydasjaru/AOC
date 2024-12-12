stacks = []

def ApplyCommand(amount: int, fr: int, to: int):
    items = stacks[fr][-1 * amount:]
    stacks[fr] = stacks[fr][:-1 * amount]
    stacks[to] = stacks[to] + items

f = open("input.txt")
line = f.readline().strip()
while line != "":
    stacks.append(list(line))
    line = f.readline().strip()

line = f.readline().strip()
while line != "":
    command = line.split(" ")
    ApplyCommand(int(command[1]), int(command[3]) - 1, int(command[5]) - 1)
    line = f.readline().strip()

for s in stacks:
    print(s[-1])
