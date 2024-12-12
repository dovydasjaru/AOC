from __future__ import annotations
import time


def FindLocation(sensors: list) -> tuple[int, int]:
    min_search_range = 0
    max_search_range = 4000000
    for y in range(min_search_range, max_search_range + 1):
        positions_range = []
        for sensor, beacon in sensors:
            beacon_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
            if abs(y - sensor[1]) <= beacon_distance:
                position_delta = beacon_distance - abs(y - sensor[1])
                positions_range.append([sensor[0] - position_delta, sensor[0] + position_delta])

        positions_range = CongregateRanges(positions_range)
        if len(positions_range) == 2:
            if positions_range[0][0] < positions_range[1][0]:
                return y, positions_range[0][1] + 1
            else:
                return y, positions_range[1][1] + 1            
        if positions_range[0][0] == min_search_range + 1:
            return y, min_search_range
        if positions_range[0][1] == max_search_range - 1:
            return y, max_search_range
    
    return 0, 0



def CalculateIsNot(sensors: list, row: int) -> int:
    positions_range = []
    beacons_at_row = []
    for sensor, beacon in sensors:
        if row == beacon[1] and beacon[0] not in beacons_at_row:
            beacons_at_row.append(beacon[0])

        beacon_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        if abs(row - sensor[1]) <= beacon_distance:
            position_delta = beacon_distance - abs(row - sensor[1])
            positions_range.append([sensor[0] - position_delta, sensor[0] + position_delta])

    congregated_positions = CongregateRanges(positions_range)

    positions_sum = 0
    for pos in congregated_positions:
        positions_sum += 1 + pos[1] - pos[0]
    
    return positions_sum - len(beacons_at_row)


def CongregateRanges(positions_range: list) -> list:
    congregated_positions = []
    while len(positions_range) > 0:
        position_range = positions_range.pop()
        for r in positions_range:
            if position_range[1] <= r[1] and position_range[0] >= r[0]:
                position_range = None
                break
            if position_range[1] >= r[1] and position_range[0] <= r[0]:
                r[0] = position_range[0]
                r[1] = position_range[1]
                position_range = None
                break
            if position_range[1] <= r[1] and position_range[1] >= r[0]:
                r[0] = position_range[0]
                position_range = None
                break
            if position_range[0] >= r[0] and position_range[0] <= r[1]:
                r[1] = position_range[1]
                position_range = None
                break
        
        if position_range is not None:
            congregated_positions.append(position_range)
    return congregated_positions


f = open("input.txt")
sensors = []
for line in f.readlines():
    line = line.strip().split(": ")
    sensor = [int(x[2:]) for x in line[0][10:].split(", ")]
    beacon = [int(x[2:]) for x in line[1][21:].split(", ")] 
    sensors.append([sensor, beacon])

ans1 = CalculateIsNot(sensors, 2000000)
print(ans1)
ans2 = FindLocation(sensors)
print(ans2[1] * 4000000 + ans2[0])