from __future__ import annotations
from math import floor


class Monkey():
    def __init__(self, items: list[int], operation, operation_param: int, test: int, results: tuple[int, int]):
        self.items = items
        self.operation = operation
        self.operation_param = operation_param
        self.test = test
        self.results = results
        self.inspected = 0
    
    def InspectItems(self, worried: int) -> list[tuple[int, int]]:
        inspected_items = []
        for item in self.items:
            if worried is not None:
                item = item % worried
            item = self.operation(item, self.operation_param)
            if worried is None:
                item = floor(item / 3)
            monkey = self.results[int(item % self.test != 0)]
            inspected_items.append((monkey, item))

        self.items = []
        self.inspected += len(inspected_items)
        return inspected_items
    
    def AddItem(self, item: int):
        self.items.append(item)


def ThrowItems(monkeys: list[Monkey], rounds: int, worried: int):
    for _ in range(rounds):
        for monkey in monkeys:
            thrown_items = monkey.InspectItems(worried)
            for item in thrown_items:
                monkeys[item[0]].AddItem(item[1])


f = open("input.txt")
monkeys: list[Monkey] = []
line = f.readline().strip()
while line != "":
    line = f.readline().strip()
    items = [int(x) for x in line[16:].split(", ")]

    line = f.readline().strip()
    operation_params = line[21:].split(" ")
    operation = None
    y = 0
    if operation_params[0] == "*":
        if operation_params[1] == "old":
            operation = lambda x, _: x * x
        else:
            operation = lambda x, y: x * y
            y = int(operation_params[1])
    else:
        operation = lambda x, y: x + y
        y = int(operation_params[1])
    
    line = f.readline().strip()
    test = int(line[19:])
    on_true = int(f.readline().strip()[25:])
    on_false = int(f.readline().strip()[26:])
    f.readline()
    line = f.readline().strip()

    monkeys.append(Monkey(items, operation, y, test, (on_true, on_false)))

# part 1
#ThrowItems(monkeys, 20, None)

# part 2
divisor = 1
for m in monkeys:
    divisor *= m.test
ThrowItems(monkeys, 10000, divisor)

thrown_amount: list[int] = []
for monkey in monkeys:
    thrown_amount.append(monkey.inspected)
print(thrown_amount)
thrown_amount.sort()
print(thrown_amount[-1] * thrown_amount[-2])
