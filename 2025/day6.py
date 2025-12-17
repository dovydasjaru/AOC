def grandTotal(numbers: list[list[int]], operations: list[str]) -> int:
  total = 0
  for i in range(len(numbers)):
    subTotal = 0
    if operations[i] == "*":
      subTotal = 1
    
    for j in range(len(numbers[i])):
      if operations[i] == "*":
        subTotal *= numbers[i][j]
      else:
        subTotal += numbers[i][j]
    
    total += subTotal
  
  return total


def convertNumbers(input: list[str]) -> list[list[int]]:
  converted = []
  numberList = [[int(number) for number in i.split()] for i in input]
  for j in range(len(numberList[0])):
    part = []
    for i in range(len(numberList)):
      part.append(numberList[i][j])
    
    converted.append(part)
  
  return converted


def convertCephalopodNumbers(input: list[str]) -> list[list[int]]:
  converted = []
  part = []

  for j in range(len(input[0])):
    number = ""
    for i in range(len(input)):
      number += input[i][j]
    
    number = number.strip()
    if number == "":
      converted.append(part)
      part = []
    else:
      part.append(int(number))
  
  converted.append(part)

  return converted


numberLines = [line[:-1] for line in open("input6.txt").readlines()]
operations = numberLines.pop().strip().split()

correctedNumbers = convertNumbers(numberLines)
print(grandTotal(correctedNumbers, operations))

correctedNumbers = convertCephalopodNumbers(numberLines)
print(grandTotal(correctedNumbers, operations))