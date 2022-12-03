from collections import Counter


def get_priority(char: str):
    if char.islower():
        return ord(char) - 96
    else:
        return ord(char) - 65 + 27


with open('input') as f:
    sacks = f.read().strip().split('\n')


def p1():
    summed = 0
    for sack in sacks:
        mid = len(sack) // 2
        left = sack[:mid]
        right = sack[mid:]
        shared = (set(left) & set(right)).pop()
        summed += get_priority(shared)

    print("p1:", summed)


def p2():
    groups = [sacks[i:i + 3] for i in range(0, len(sacks), 3)]

    sum = 0
    for group in groups:
        cmp_sacks = [set(s) for s in group]
        s1, s2, s3 = cmp_sacks
        shared = (s1 & s2 & s3).pop()
        sum += get_priority(shared)
    print("p2:", sum)


p1()
p2()
