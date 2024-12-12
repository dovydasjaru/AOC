
class Computer():
    def __init__(self, commands: list):
        self.strength = 0
        self.x = 1
        self.cycle = 0
        self.commands = commands        
    
    def DoStuff(self) -> int:
        line = []
        for command in self.commands:
            if command is None:
                self.cycle
                line = self.MoveTickPixel(line)
            else:
                line = self.MoveTickPixel(line)
                line = self.MoveTickPixel(line)
                self.x += int(command)

        return self.strength
    
    def MoveTickPixel(self, line: list) -> list:
        position = self.cycle % 40
        self.cycle += 1

        if self.cycle % 40 == 20:
            self.strength += self.cycle * self.x
        
        if position >= self.x - 1 and position <= self.x + 1:
            line.append("#")
        else:
            line.append(".")
        
        if position == 39:
            print("".join(line))
            return []
        
        return line


f = open("input.txt")
commands = []
time = 0
for line in f.readlines():
    line = line.strip().split(" ")
    if line[0] == "noop":
        commands.append(None)
    else:
        commands.append(int(line[1]))

c = Computer(commands)
print(c.DoStuff())