def CaclulateTokens(aPresses: int, bPresses: int) -> int:
    return aPresses * 3 + bPresses


def isNumbnersInt(a, b) -> bool:
    return a % 1 == 0 and b % 1 == 0 and a >= 0 and b >= 0


def FindMinimum(machine: list[int]) -> int:
    aPresses = (machine[5] * machine[2] - machine[4] * machine[3]) / (machine[1] * machine[2] - machine[0] * machine[3])
    bPresses = (machine[4] - aPresses * machine[0]) / machine[2]
    if isNumbnersInt(aPresses, bPresses):
        return CaclulateTokens(int(aPresses), int(bPresses))

    return 0


clawMachines: list[list[int]] = []
input = open("input13.txt").readlines()
for i in range(0, len(input), 4):
    a = input[i].strip()[12:].split(", Y+")
    b = input[i + 1].strip()[12:].split(", Y+")
    prize = input[i + 2].strip()[9:].split(", Y=")
    clawMachines.append([int(a[0]), int(a[1]), int(b[0]), int(b[1]), int(prize[0]), int(prize[1])])

totalTokens = 0
for machine in clawMachines:
    totalTokens += FindMinimum(machine)

print(totalTokens)

errorFix = 10000000000000
for machine in clawMachines:
    machine[4] += errorFix
    machine[5] += errorFix

totalTokens = 0
for machine in clawMachines:
    totalTokens += FindMinimum(machine)

print(totalTokens)