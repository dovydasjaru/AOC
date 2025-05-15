def CalculateNextSecret(secret: int) -> int:
    result = secret << 6 # multiply by 2^6 = 64
    secret = result ^ secret # mix
    secret &= 16777216 - 1 # take bitwise which in this case equals to modulus as 2^24 = 16777216

    result = secret >> 5 # divide by 2^5 = 32 and take the whole part
    secret = result ^ secret # mix
    secret &= 16777216 - 1 # take bitwise which in this case equals to modulus as 2^24 = 16777216

    result = secret << 11 # multiply by 2^11 = 2048
    secret = result ^ secret # mix
    secret &= 16777216 - 1 # take bitwise which in this case equals to modulus as 2^24 = 16777216

    return secret


def GetDifferences(sequence: list[int]) -> list[int]:
    differences = []
    for i in range(len(sequence) - 1):
        differences.append(sequence[i + 1] - sequence[i])
    
    return differences


def GeneratePossibleDifferences() -> set[tuple[int]]:
    sequences: list[tuple[int]] = []
    for i in range(100000):
        sequences.append((i // 10000, (i % 10000) // 1000, (i % 1000) // 100, (i % 100) // 10, i % 10))
    
    differences: set[tuple[int]] = set()
    for s in sequences:
        differences.add((s[1] - s[0], s[2] - s[1], s[3] - s[2], s[4] - s[3]))
    
    return differences


def pruneDifferences(differences: set[tuple[int]]) -> list[tuple[int]]:
    good: list[tuple[int]] = []
    for diff in differences:
        if sum(diff) >= 0:
            good.append(diff)

    return good


def CalculateBananas(buyerInfo: list[dict[tuple[int], int]], testable: tuple[int]) -> int:
    bananas = 0
    for buyer in buyerInfo:
        bananas += buyer.get(testable, 0)
        
    return bananas


def FindMostBananas(buyerInfos: list[dict[tuple[int], int]]) -> int:
    currentMaximum = 0
    possibleDifferences = GeneratePossibleDifferences()
    prunedDifferences = pruneDifferences(possibleDifferences)
    print("Got all viable differences: ", len(prunedDifferences))
    
    for diff in prunedDifferences:
        bananas = CalculateBananas(buyerInfos, diff)
        if bananas > currentMaximum:
            currentMaximum = bananas
    
    return currentMaximum


initialNumbers = []
for line in open("input22.txt").readlines():
    initialNumbers.append(int(line.strip()))

ans = 0
buyerSequences: list[list[int]] = []
for number in initialNumbers:
    sequence = [number % 10]
    for _ in range(2000):
        number = CalculateNextSecret(number)
        sequence.append(number % 10)
    
    ans += number
    buyerSequences.append(sequence)

print(ans)

buyerDicts: list[dict[tuple[int], int]] = []
for sequence in buyerSequences:
    differences = GetDifferences(sequence)
    buyerDict: dict[tuple[int], int] = {}
    for i in range(len(differences) - 3):
        four = (differences[i], differences[i + 1], differences[i + 2], differences[i + 3])
        if buyerDict.get(four, None) != None:
            continue

        buyerDict[four] = sequence[i + 4]
    
    buyerDicts.append(buyerDict)

print(FindMostBananas(buyerDicts))