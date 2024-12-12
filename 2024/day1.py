list1 = []
list2 = []
dict2 = {}
for line in open("input1.txt").readlines():
    l = line.split("   ")
    list1.append(int(l[0]))
    list2.append(int(l[1]))
    if dict2.get(int(l[1]), None) is None:
        dict2[int(l[1])] = 1
    else:
        dict2[int(l[1])] += 1

list1.sort()
list2.sort()

ans1 = 0
ans2 = 0
for i in range(len(list1)):
    ans1 += abs(list2[i] - list1[i])
    ans2 += list1[i] * dict2.get(list1[i], 0)

print(ans1)
print(ans2)