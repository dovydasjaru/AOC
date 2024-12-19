def CountPossibleArrangements(towels: set[str], pattern: str, longestTowel: int, lengthPatternCount: list[tuple[int]] = []) -> int:
    if len(pattern) == 0:
        return 1
    filtered = list(filter(lambda x: x[0] == len(pattern), lengthPatternCount))
    if len(filtered) == 1:
        return filtered[0][1]
    if len(filtered) > 1:
        raise Exception("Bad calculation")
    
    count = 0
    maxLength = longestTowel
    if longestTowel > len(pattern):
        maxLength = len(pattern)
    for i in range(maxLength, 0, -1):
        if towels.issuperset(set([pattern[:i]])):
            count += CountPossibleArrangements(towels, pattern[i:], longestTowel, lengthPatternCount)
    
    lengthPatternCount.append((len(pattern), count))
    return count


input = open("input19.txt").readlines()
towels: set[str] = set(input[0].strip().split(", "))
longestTowel: int = max(map(len, input[0].strip().split(", ")))
patterns: list[str] = []
for i in range(2, len(input)):
    patterns.append(input[i].strip())

i = 0
possiblePatterns = 0
countOfAllPatterns = 0
for pattern in patterns:
    i += 1
    print("Current pattern:", i, "/", len(patterns))
    possibleArrangements = CountPossibleArrangements(towels, pattern, longestTowel, [])
    if possibleArrangements > 0:
        possiblePatterns += 1
        countOfAllPatterns += possibleArrangements

print(possiblePatterns)
print(countOfAllPatterns)