import numpy as np


def Travel(path: list) -> np.ndarray:
    spread = GetTravelSpread(path)
    tail_path = np.zeros([spread[3] - spread[1] + 1, spread[2] - spread[0] + 1])
    head_position = [-spread[0], -spread[1]]
    tail_position = [-spread[0], -spread[1]]
    tail_path[tail_position[1], tail_position[0]] = 1

    for p in path:
        if p[0] == "R":
            head_position[0] += p[1]
            if head_position[0] > tail_position[0] + 1:
                tail_path[head_position[1], tail_position[0] + 1:head_position[0]] = 1
                tail_position[0] = head_position[0] - 1
                tail_position[1] = head_position[1]
        elif p[0] == "L":
            head_position[0] -= p[1]
            if head_position[0] < tail_position[0] - 1:
                tail_path[head_position[1], head_position[0] + 1:tail_position[0]] = 1
                tail_position[0] = head_position[0] + 1
                tail_position[1] = head_position[1]
        elif p[0] == "D":
            head_position[1] += p[1]
            if head_position[1] > tail_position[1] + 1:
                tail_path[tail_position[1] + 1:head_position[1], head_position[0]] = 1
                tail_position[0] = head_position[0]
                tail_position[1] = head_position[1] - 1
        elif p[0] == "U":
            head_position[1] -= p[1]
            if head_position[1] < tail_position[1] - 1:
                tail_path[head_position[1] + 1:tail_position[1], head_position[0]] = 1
                tail_position[0] = head_position[0]
                tail_position[1] = head_position[1] + 1

    return tail_path


def GenericTravel(path: list, rope_length: int) -> np.ndarray:
    spread = GetTravelSpread(path)
    rope = [[-spread[1], -spread[0]] for _ in range(rope_length)]
    tail_path = np.zeros([spread[3] - spread[1] + 1, spread[2] - spread[0] + 1])
    tail_path[rope[-1][0], rope[-1][1]] = 1

    for p in path:
        direction = [0, 0]
        if p[0] == "R":
            direction = [0, 1]
        elif p[0] == "L":
            direction = [0, -1]
        elif p[0] == "D":
            direction = [1, 0]
        elif p[0] == "U":
            direction = [-1, 0]
        
        for _ in range(p[1]):
            rope = MoveRope(direction, rope)
            tail_path[rope[-1][0], rope[-1][1]] = 1

    return tail_path


def GetTravelSpread(path: list) -> list:
    max = [0, 0, 0, 0]
    current = [0, 0]
    for p in path:
        if p[0] == "R":
            current[0] += p[1]
            if current[0] > max[2]:
                max[2] = current[0]
        elif p[0] == "L":
            current[0] -= p[1]
            if current[0] < max[0]:
                max[0] = current[0]
        elif p[0] == "D":
            current[1] += p[1]
            if current[1] > max[3]:
                max[3] = current[1]
        elif p[0] == "U":
            current[1] -= p[1]
            if current[1] < max[1]:
                max[1] = current[1]
        
    return max


def MoveRope(direction: list, rope: list) -> list:
    rope[0][0] += direction[0]
    rope[0][1] += direction[1]
    for i in range(len(rope) - 1):
        if IsTouching(rope[i], rope[i + 1]):
            return rope
        rope[i + 1] = KeepUpTail(rope[i], rope[i + 1])

    return rope


def IsTouching(knot1: list, knot2: list) -> bool:
    return abs(knot1[0] - knot2[0]) < 2 and abs(knot1[1] - knot2[1]) < 2


def KeepUpTail(head: list, tail: list) -> list:
    difference = [(head[0] - tail[0]) / 2, (head[1] - tail[1]) / 2]
    difference = [1 if v > 0 else -1 if v < 0 else 0 for v in difference]
    
    return [difference[0] + tail[0], difference[1] + tail[1]]


f = open("input.txt")
path = []
for line in f.readlines():
    p = line.strip().split(" ")
    path.append([p[0], int(p[1])])

print(np.count_nonzero(Travel(path)))
print(np.count_nonzero(GenericTravel(path, 10)))