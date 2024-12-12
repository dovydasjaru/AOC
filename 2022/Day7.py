from __future__ import annotations

f = open("input.txt")

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.directories = {}
        self.files = {}
        self.file_size = 0
        self.size = -1

    def AddDirectory(self, name: str, dir: Directory):
        self.directories[name] = dir
        dir.SetFather(self)
    
    def GetDirectory(self, name: str) -> Directory:
        return self.directories[name]
    
    def AddFile(self, size: int):
        self.file_size += size
    
    def SetFather(self, dir: Directory):
        self.father = dir
    
    def GetFather(self) -> Directory:
        return self.father
    
    def GetSize(self) -> int:
        if self.size >= 0:
            return self.size
        
        self.size = 0
        for value in self.directories.values():
            self.size += value.GetSize()
        
        self.size += self.file_size
        
        return self.size


root_directory = Directory("/")
current_directory = root_directory
all_directories = [root_directory]
f.readline()

for line in f.readlines():
    line = line.strip().split(" ")
    if line[0] == "$" and line[1] == "cd":
        if line[2] == "..":
            current_directory = current_directory.GetFather()
        else:
            current_directory = current_directory.GetDirectory(line[2])
    elif line[0] == "dir":
        new_directory = Directory(line[1])
        current_directory.AddDirectory(line[1], new_directory)
        all_directories.append(new_directory)
    elif line[0].isnumeric():
        current_directory.AddFile(int(line[0]))
    elif " ".join(line) != "$ ls":
        raise Exception("SHIET: " + " ".join(line))

possible = -1
required_minimum = 30000000 - (70000000 - root_directory.GetSize())
for dir in all_directories:
    if dir.GetSize() >= required_minimum and (possible > dir.GetSize() or possible == -1):
        possible = dir.GetSize()

print(possible) # 8582270 too high