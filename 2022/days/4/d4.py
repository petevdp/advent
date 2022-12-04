with open('input') as f:
    ranges = [tuple(line.strip().split(',')) for line in f]


def conv_range(_range):
    start, end = _range
    return set(range(start, end + 1))


def compare_p1(s1, s2):
    inter = s1 & s2
    return inter == s1 or inter == s2


def compare_p2(s1, s2):
    return len(s1 & s2) > 0


count_p1 = 0
count_p2 = 0
for i, line in enumerate(ranges):
    r1, r2 = [*(tuple(map(int, r.split('-'))) for r in line)]
    s1, s2 = conv_range(r1), conv_range(r2)
    if compare_p1(s1, s2):
        count_p1 += 1
    if compare_p2(s1, s2):
        count_p2 += 1

print("p1: ", count_p1)
print("p2: ", count_p2)
