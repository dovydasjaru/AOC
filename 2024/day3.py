import re

ans1 = 0
ans2 = 0
is_active = True
for line in open("input3.txt").readlines():
    correct_commands = re.findall("mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)", line)
    for command in correct_commands:
        if command == "do()": 
            is_active = True
            continue
        if command == "don't()":
            is_active = False
            continue

        numbers = list(map(int, (command[4:-1]).split(",")))
        ans1 += numbers[0] * numbers[1]
        if is_active:
            ans2 += numbers[0] * numbers[1]

print(ans1)
print(ans2)