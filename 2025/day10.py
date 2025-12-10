from itertools import combinations


class Machine:
  indicatorDiagram: tuple[bool]
  buttons: tuple[tuple[int]]
  joltage: tuple[int]

  def __init__(self, indicatorDiagram: str, buttons: list[list[str]], joltage: str):
    self.indicatorDiagram = tuple(True if indicator == "#" else False for indicator in indicatorDiagram)
    self.buttons = tuple(tuple(int(wire) for wire in button) for button in buttons)
    self.joltage = tuple(int(jolt) for jolt in joltage.split(","))


def pressButton(indicators: list[bool], button: tuple[int]) -> list[bool]:
  for wire in button:
    indicators[wire] = not indicators[wire]
  
  return indicators


def findFewestPressesIndicators(machine: Machine) -> int:
  buttonIds = list(range(0, len(machine.buttons)))
  presses = 1
  while presses <= len(machine.buttons):
    for combination in combinations(buttonIds, presses):
      indicators = [False] * len(machine.indicatorDiagram)
      for buttonId in combination:
        pressButton(indicators, machine.buttons[buttonId])
      
      if tuple(indicators) == machine.indicatorDiagram:
        return presses
    
    presses += 1
  
  return 0


def findFewestPressesJoltages(machine: Machine) -> int:


machines: list[Machine] = []
for line in open("input10.txt").readlines():
  input = line.strip().split(" ")
  machines.append(Machine(input[0][1:-1], [i[1:-1].split(",") for i in input[1:-1]], input[-1][1:-1]))

answer = 0
for m in machines:
  answer += findFewestPressesIndicators(m)
print(answer)

answer = 0
for m in machines:
  answer += findFewestPressesJoltages(m)
print(answer)
