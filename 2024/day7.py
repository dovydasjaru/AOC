def isTrueEquation(value, operands, currentValue) -> bool:
    if currentValue > value:
        return False
    if currentValue == value and len(operands) == 0:
        return True
    if len(operands) == 0:
        return False
    
    return (isTrueEquation(value, operands[1:], currentValue * operands[0]) or 
        isTrueEquation(value, operands[1:], currentValue + operands[0]))

def isTrueEquationConcat(value, operands, currentValue) -> bool:
    if currentValue > value:
        return False
    if currentValue == value and len(operands) == 0:
        return True
    if len(operands) == 0:
        return False
    
    return (isTrueEquationConcat(value, operands[1:], int(str(currentValue) + str(operands[0]))) or
        isTrueEquationConcat(value, operands[1:], currentValue * operands[0]) or
        isTrueEquationConcat(value, operands[1:], currentValue + operands[0]))


equations: list[list[int]] = []
for line in open("input7.txt").readlines():
    numbers = line.strip().split(" ")
    numbers[0] = numbers[0][:-1]
    equations.append(list(map(int, numbers)))

ans1 = 0
ans2 = 0
for equation in equations:
    value = equation.pop(0)
    firstOperand = equation.pop(0)
    if isTrueEquation(value, equation, firstOperand):
        ans1 += value
        ans2 += value
    elif isTrueEquationConcat(value, equation, firstOperand):
        ans2 += value

print(ans1)
print(ans2)
