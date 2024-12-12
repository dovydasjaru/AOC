choices = {"A": 1, "B": 2, "C": 3}

def CalculateScore(oponent: str, you: str) -> int:
    score = choices[you]
    
    if you == oponent:
        score += 3
    elif choices[oponent] - choices[you] == -1 or choices[oponent] - choices[you] == 2:
        score += 6
    
    return score


def Convert(oponent: str, result: str) -> str:
    if result == "X":
        c = (choices[oponent] + 1) % 3 + 1
        return list(choices.keys())[list(choices.values()).index(c)]
    elif result == "Y":
        return oponent
    else:
        c = (choices[oponent]) % 3 + 1
        return list(choices.keys())[list(choices.values()).index(c)]


f = open("input.txt")

total = 0
for line in f.readlines():
    line = line.strip()
    you = Convert(line[0], line[2])
    total += CalculateScore(line[0], you)

print(total)
