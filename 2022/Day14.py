from __future__ import annotations
import numpy as np
import sys
np.set_printoptions(threshold = sys.maxsize)


def BuildRockMap(rocks: list[list[tuple[int, int]]], max_x: int, max_y: int) -> np.ndarray:
    rock_map = np.full((max_y + 2, max_x + 2 + max_y), False, bool)
    for rock in rocks:
        last_y, last_x = rock.pop(0)
        for r in rock:
            y, x = r
            if last_y > y:
                y = last_y
                last_y = r[0]
            if last_x > x:
                x = last_x
                last_x = r[1]
            
            rock_map[last_y:y + 1, last_x:x + 1] = True
            last_y, last_x = r

    return rock_map


def DropSandUntilEnd(rock_map: np.ndarray) -> int:
    sand_used = 0
    x = 500
    y = 0
    fall_path = []
    done = False
    while not done:
        if y + 1 == rock_map.shape[0]:
            done = True
            continue
        
        fall_path.append((y, x))

        if not rock_map[y + 1, x]:
            y += 1
            continue
        if not rock_map[y + 1, x - 1]:
            y += 1
            x -= 1
            continue
        if not rock_map[y + 1, x + 1]:
            y += 1
            x += 1
            continue
        
        if y == 0 and x == 500:
            done = True
        else:
            fall_path.pop()
        
        rock_map[y, x] = True
        y, x = fall_path.pop()        
        sand_used += 1
        
    return sand_used


def printRocks(rock_map: np.ndarray):
    for line in rock_map:
        print("".join(["#" if x else "." for x in line[350:]]))


f = open("input.txt")
rock_coordinates = []
max_x = 0
max_y = 0
for line in f.readlines():
    line = line.strip().split(" -> ")
    rock_coordinates.append([])

    for l in line:
        x, y = [int(a) for a in l.split(",")]

        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

        rock_coordinates[-1].append((y, x))

rock_map = BuildRockMap(rock_coordinates, max_x, max_y)
rock_map2 = np.vstack([rock_map, np.full(rock_map.shape[1], True, bool)])
ans1 = DropSandUntilEnd(rock_map)
ans2 = DropSandUntilEnd(rock_map2)

print(ans1)
print(ans2)
