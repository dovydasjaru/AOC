def GetMarkerPosition(data: list, markerSize: int) -> int:
    offset = markerSize
    while not IsMarker(data[offset - markerSize:offset]):
        offset += 1
    
    return offset


def IsMarker(data: list) -> bool:
    unique = []
    for char in data:
        if char in unique:
            return False
        unique.append(char)
    return True


f = open("input.txt")
data = []
for line in f.readlines():
    data = data + list(line.strip())

print(GetMarkerPosition(data, 14))