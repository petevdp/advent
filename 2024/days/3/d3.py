import sys
import re

with open(sys.argv[1]) as f:
    T = f.read()

def solve():
    matches = re.findall(r"(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))", T)
    p1 = 0
    p2 = 0
    do = True
    for m in matches:
        if m[-2] == "do()":
            do = True
            continue
        if m[-1] == "don't()":
            do = False
            continue
        a,b = map(int, m[1:3])
        p1 += a * b
        if do: p2 += a * b
    print("p1", p1)
    print("p2", p2)


if __name__ == '__main__':
    solve()
