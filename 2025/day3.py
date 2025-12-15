def findHighestJoltage(bank: list[int], batteryCount: int) -> int:
  highestJoltage = 0
  batteryIndexStart = -1
  for batteryNumber in range(batteryCount):
    highestBattery = 0
    for i in range(batteryIndexStart + 1, len(bank) - (batteryCount - batteryNumber - 1)):
      if highestBattery < bank[i]:
        highestBattery = bank[i]
        batteryIndexStart = i
    
    highestJoltage = highestJoltage * 10 + bank[batteryIndexStart]
  
  return highestJoltage


banks = [ [ int(character) for character in line.strip() ] for line in open("input3.txt").readlines() ]

answer = 0
for bank in banks:
  answer += findHighestJoltage(bank, 2)
print(answer)

answer = 0
for bank in banks:
  answer += findHighestJoltage(bank, 12)
print(answer)