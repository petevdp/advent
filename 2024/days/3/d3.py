import sys
import re

with open(sys.argv[1]) as f:
    T = f.read()

def solve():
    matches = re.findall(r"((mul)|(do)|(don't))\(((\d+),(\d+))?\)", T)
    p1 = 0
    p2 = 0
    do = True
    for m in matches:
        if m[0] == "do":
            do = True
            continue
        if m[0] == "don't":
            do = False
            continue
        a,b = map(int, m[-2:])
        p1 += a * b
        if not do: continue
        p2 += a * b
    print("p1", p1)
    print("p2", p2)


if __name__ == '__main__':
    solve()
