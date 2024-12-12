from __future__ import annotations
import numpy as np


def FloodFill(rock: np.ndarray) -> np.ndarray:
    fill = np.full(rock.shape, False, bool)

    fill[0, :, :] = np.full(rock.shape[1:], True, bool)
    for z in range(1, rock.shape[0] - 1):
        fill[z, :, :] = np.logical_and(fill[z - 1, :, :], np.logical_not(rock[z, :, :]))
        fill[z, :, :] = FloodFillLayer(rock[z, :, :], fill[z, :, :])
    
    fill[-1, :, :] = np.full(rock.shape[1:], True, bool)
    for z in range(rock.shape[0] - 2, 1, -1):
        fill[z, :, :] = np.logical_or(fill[z, :, :], np.logical_and(fill[z + 1, :, :], np.logical_not(rock[z, :, :])))
        fill[z, :, :] = FloodFillLayer(rock[z, :, :], fill[z, :, :])
    
    return fill


def FloodFillLayer(rock: np.ndarray, fill: np.ndarray) -> np.ndarray:
    filling = True
    while filling:
        filling = False
        for y in range(1, rock.shape[0] - 1):
            for x in range(1, rock.shape[1] - 1):
                if not fill[y, x] and not rock[y, x]:
                    if fill[y, x - 1]:
                        fill[y, x] = True
                        filling = True
                    elif fill[y, x + 1]:
                        fill[y, x] = True
                        filling = True
                    elif fill[y - 1, x]:
                        fill[y, x] = True
                        filling = True
                    elif fill[y + 1, x]:
                        fill[y, x] = True
                        filling = True
    
    return fill


def CalculateArea(rock: np.ndarray, fill: np.ndarray) -> int:
    area = 0
    for z in range(1, rock.shape[0] - 1):
        for y in range(1, rock.shape[1] - 1):
            for x in range(1, rock.shape[2] - 1):
                if rock[z, y, x]:
                    if fill[z, y, x - 1]:
                        area += 1
                    if fill[z, y, x + 1]:
                        area += 1
                    if fill[z, y - 1, x]:
                        area += 1
                    if fill[z, y + 1, x]:
                        area += 1
                    if fill[z - 1, y, x]:
                        area += 1
                    if fill[z + 1, y, x]:
                        area += 1

    return area


def PrintRock(rock: np.ndarray, fill: np.ndarray):
    for z in range(rock.shape[0]):
        for y in range(rock.shape[1]):
            line = []
            failed = False
            for x in range(rock.shape[2]):
                if rock[z, y, x] and fill[z, y, x]:
                    failed = True
                    line.append("S")
                elif rock[z, y, x]:
                    line.append("#")
                elif fill[z, y, x]:
                    line.append("-")
                else:
                    line.append(".")
            
            print("".join(line))
            if failed:
                raise Exception("Failed flood fill")
        print()


f = open("input.txt")
positions: list[tuple[int, int, int]] = []
biggest_coordinate = [0, 0, 0]
for line in f.readlines():
    x, y, z = [int(x) for x in line.strip().split(",")]
    if biggest_coordinate[0] < x:
        biggest_coordinate[0] = x
    if biggest_coordinate[1] < y:
        biggest_coordinate[1] = y
    if biggest_coordinate[2] < z:
        biggest_coordinate[2] = z
    positions.append((x, y, z))

rock = np.full((biggest_coordinate[2] + 3, biggest_coordinate[1] + 3, biggest_coordinate[0] + 3), False, bool)
for x, y, z in positions:
    rock[z + 1, y + 1, x + 1] = True

ans1 = CalculateArea(rock, np.logical_not(rock))
fill = FloodFill(rock)
ans2 = CalculateArea(rock, fill)

print(ans1)
print(ans2)