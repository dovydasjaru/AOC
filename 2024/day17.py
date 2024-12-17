class Computer:
    def __init__(self, regA: int, regB: int, regC: int):
        self.regA = regA
        self.regB = regB
        self.regC = regC
        
    def GetComboOperand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.regA
            case 5:
                return self.regB
            case 6:
                return self.regC
            
        raise Exception("Received unexpected combo operand: " + str(operand))


    def ExecuteProgram(self, program: list[int], pointer: int) -> list[int]:
        output = []
        while pointer < len(program) - 1:
            opcode = program[pointer]
            operand = program[pointer + 1]
            pointer += 2

            match opcode:
                case 0:
                    self.regA = self.regA // (2 ** self.GetComboOperand(operand))
                case 1:
                    self.regB = self.regB ^ operand
                case 2:
                    self.regB = self.GetComboOperand(operand) % 8
                case 3:
                    if self.regA != 0:
                        pointer = operand
                case 4:
                    self.regB = self.regB ^ self.regC
                case 5:
                    output.append(self.GetComboOperand(operand) % 8)
                case 6:
                    self.regB = self.regA // (2 ** self.GetComboOperand(operand))
                case 7:
                    self.regC = self.regA // (2 ** self.GetComboOperand(operand))

        return output


input = open("input17.txt").readlines()
regA = int(input[0].strip()[12:])
regB = int(input[1].strip()[12:])
regC = int(input[2].strip()[12:])
program = list(map(int, input[4].strip()[9:].split(",")))

computer = Computer(regA, regB, regC)
output = computer.ExecuteProgram(program, 0)
print(",".join(map(str, output)))

possible = [0]
for i in range(len(program)):
    newPossible = []
    for p in possible:
        start = p * 8
        for j in range(8):
            computer.regA = start + j
            computer.regB = 0
            computer.regC = 0
            output = computer.ExecuteProgram(program, 0)
            conforms = True
            for x in range(-1, (i + 2) * -1, -1):
                if output[x] != program[x]:
                    conforms = False
            if conforms:
                newPossible.append(start + j)
    possible = newPossible

print(min(possible))
