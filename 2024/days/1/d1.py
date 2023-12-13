from collections import defaultdict
L = []
R = []
with open('days/1/input_d1.txt') as f:
    for line in f:
        l, r = map(int, line.strip().split())
        L.append(l)
        R.append(r)

L = sorted(L)
R = sorted(R)

def part1():

    sum = 0
    for i in range(len(L)):
        diff = abs(R[i] - L[i])
        sum += diff
    print("p1", sum)

def part2():
    counts = defaultdict(lambda: 0)
    for n in R:
        counts[n] += 1

    sum = 0
    for n in L:
        sum += n * counts[n]

    print("p2", sum)


if __name__ == '__main__':
    part1()
    part2()
