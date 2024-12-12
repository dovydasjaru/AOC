def isCorrect(pages: list[str], rules: set[str]) -> bool:
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if not rules.issuperset([pages[i] + "|" + pages[j]]):
                return False
    
    return True


def fixManual(pages: list[str], rules: set[str]) -> list[str]:
    fixed = [pages[0]]
    for i in range(1, len(pages)):
        for j in range(len(fixed)):
            if not rules.issuperset([fixed[j] + "|" + pages[i]]):
                fixed.insert(j, pages[i])
                break
        if len(fixed) == i:
            fixed.append(pages[i])
    
    return fixed


input = open("input5.txt").readlines()
page_position = -1
rules = set()
for i in range(len(input)):
    if input[i] == "\n":
        page_position = i + 1
        break

    rules.add(input[i].strip())

manuals = []
for i in range(page_position, len(input)):
    manuals.append(input[i].strip().split(","))

ans1 = 0
ans2 = 0
for i in range(len(manuals)):
    if isCorrect(manuals[i], rules):
        ans1 += int(manuals[i][int((len(manuals[i])) / 2)])
    else:
        fixed_manual = fixManual(manuals[i], rules)
        ans2 += int(fixed_manual[int((len(fixed_manual)) / 2)])

print(ans1)
print(ans2)