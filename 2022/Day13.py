from __future__ import annotations


def SortPackets(packets: list, first: int, last: int):
    if first < last:
        middle = Partition(packets, first, last)
        SortPackets(packets, first, middle - 1)
        SortPackets(packets, middle + 1, last)


def Partition(packets: list, first: int, last: int) -> int:
    pivot = packets[first]
    left = first + 1
    right = last

    done = False
    while not done:
        while left <= right and IsLess(packets[left], pivot):
            left += 1
        while left <= right and IsLess(pivot, packets[right]):
            right -= 1

        if right < left:
            done = True
        else:
            temp = packets[left]
            packets[left] = packets[right]
            packets[right] = temp
    
    packets[first] = packets[right]
    packets[right] = pivot

    return right


def IsLess(packet1: list, packet2: list) -> bool | None:
    for i in range(min(len(packet1), len(packet2))):
        if type(packet1[i]) is int and type(packet2[i]) is int:
            if packet1[i] < packet2[i]:
                return True
            if packet1[i] > packet2[i]:
                return False
            continue
        
        if type(packet1[i]) is list and type(packet2[i]) is list:
            result = IsLess(packet1[i], packet2[i])
            if result is not None:
                return result
            continue
        
        result = None
        if type(packet1[i]) is int:
            result = IsLess([packet1[i]], packet2[i])
        else:
            result = IsLess(packet1[i], [packet2[i]])
        if result is not None:
            return result
        
    if len(packet1) < len(packet2):
        return True
    if len(packet1) > len(packet2):
        return False

    return None


def ReadPacket(line: str) -> list:
    packet = []
    if line[0] == "[" and line[-1] == "]" and len(line) > 2:
        items = SplitLine(line[1:-1])
        for item in items:
            if item.isnumeric():
                packet.append(int(item))
            else:
                packet.append(ReadPacket(item))

    return packet


def SplitLine(line: str) -> list[str]:
    items = []
    bracket = 0
    start = 0
    end = 0
    for c in line:
        if c == "[":
            bracket += 1
        elif c == "]":
            bracket -= 1
        elif c == "," and bracket == 0:
            items.append(line[start:end])
            start = end + 1

        end += 1
    
    items.append(line[start:end])
    return items


f = open("input.txt")
packet_pairs: list[tuple[list, list]] = []
dividers = [[[2]], [[6]]]
packets = [dividers[0], dividers[1]]
line = f.readline().strip()
while line != "":
    packet1 = ReadPacket(line)
    packet2 = ReadPacket(f.readline().strip())
    packet_pairs.append((packet1, packet2))
    packets.append(packet1)
    packets.append(packet2)

    f.readline()
    line = f.readline().strip()

answer1 = 0
for i in range(len(packet_pairs)):
    if IsLess(packet_pairs[i][0], packet_pairs[i][1]):
        answer1 += i + 1

print(answer1)

SortPackets(packets, 0, len(packets) - 1)
answer2 = 1
for i in range(len(packets)):
    if packets[i] == dividers[0]:
        answer2 *= i + 1
    if packets[i] == dividers[1]:
        answer2 *= i + 1

print(answer2)