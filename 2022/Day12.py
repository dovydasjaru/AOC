f = open("input.txt")
height_map = []
start = []
end = []
y = 0
for line in f.readlines():
    line = line.strip()
    height_map.append([])
    x = 0
    for position in line:
        if position == 'S':
            position = 'a'
            start = [y, x]
        if position == 'E':
            position = 'z'
            end = [y, x]
        
        height_map[y].append(ord(position) - 97)
        x += 1
    
    y += 1

print(height_map)
print()
print(start, end)

# part 1 done by hand answer was 383
# part 2 done by hand answer was 377

