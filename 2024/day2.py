def isSafe(report: list[int]) -> tuple[bool, int]:
    direction = report[0] - report[1] < 0
    for i in range(len(report) - 1):
        change = report[i] - report[i + 1]
        if change == 0 or (change < 0) != direction or abs(change) > 3:
            return (False, i)
    
    return (True, None)

ans1 = 0
ans2 = 0
for line in open("input2.txt").readlines():
    report = list(map(int, line.strip().split(" ")))
    result = isSafe(report)
    if result[0]:
        ans1 += 1
        ans2 += 1
    elif (isSafe(report[:result[1]] + report[result[1] + 1:])[0] or isSafe(report[:result[1] + 1] + report[result[1] + 2:])[0] or
        isSafe(report[1:])[0]):
        ans2 += 1

print(ans1)
print(ans2)
