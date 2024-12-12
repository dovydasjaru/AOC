def search1(input: list[str]) -> int:
    count = 0
    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] == "X":
                if i > 2 and input[i - 1][j] == "M" and input[i - 2][j] == "A" and input[i - 3][j] == "S":
                    count += 1
                if i > 2 and j < len(input[i]) - 3 and input[i - 1][j + 1] == "M" and input[i - 2][j + 2] == "A" and input[i - 3][j + 3] == "S":
                    count += 1
                if j < len(input[i]) - 3 and input[i][j + 1] == "M" and input[i][j + 2] == "A" and input[i][j + 3] == "S":
                    count += 1
                if i < len(input) - 3 and j < len(input[i]) - 3 and input[i + 1][j + 1] == "M" and input[i + 2][j + 2] == "A" and input[i + 3][j + 3] == "S":
                    count += 1
                if i < len(input) - 3 and input[i + 1][j] == "M" and input[i + 2][j] == "A" and input[i + 3][j] == "S":
                    count += 1
                if i < len(input) - 3 and j > 2 and input[i + 1][j - 1] == "M" and input[i + 2][j - 2] == "A" and input[i + 3][j - 3] == "S":
                    count += 1
                if j > 2 and input[i][j - 1] == "M" and input[i][j - 2] == "A" and input[i][j - 3] == "S":
                    count += 1
                if i > 2 and j > 2 and input[i - 1][j - 1] == "M" and input[i - 2][j - 2] == "A" and input[i - 3][j - 3] == "S":
                    count += 1
    
    return count

def search2(input: list[str]) -> int:
    count = 0
    for i in range(1, len(input) - 1):
        for j in range(1, len(input[i]) - 1):
            if input[i][j] == "A":
                corners = [input[i + 1][j + 1], input[i - 1][j + 1], input[i - 1][j - 1], input[i + 1][j - 1]]
                if corners in [["M", "M", "S", "S"], ["S", "M", "M", "S"], ["S", "S", "M", "M"], ["M", "S", "S", "M"]]:
                    count += 1
                
    return count


input: list[str] = []
for line in open("input4.txt").readlines():
    input.append(line.strip())

print(search1(input))
print(search2(input))

