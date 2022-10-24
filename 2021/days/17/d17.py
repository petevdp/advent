"""
in 1d:

for every point lp in interval x1..x2


f(x) = sum((7 - n) for n in range(x+1))
f(x) = sum((v - n) for n in range(x+1))
f(x) = sum((v) for n in range(x+1)) + (sum(-n for n in range(x+1)))
f(x) = v^(x+1) + (sum(-n for n in range(x+1)))
f(x) = v^(x+1) + (sum(-n for n in range(x+1)))
d = v^(x+1) + (sum(-n for n in range(x+1)))

root(d, x + 1) = v + root(sum(-n for n in range(x+1)))
root(d, x + 1) - root(sum(-n for n in range(x+1)) = v

v(x) = root(d, x + 1) - root(sum(-n for n in range(x+1), x+1)
v0 = root(d, 0 + 1) - root(sum(-n for n in range(x+1), x+1)
v0 = root(d, 0 + 1) - root(sum(-n for n in range(x+1), x+1)


"""
import math
from collections import defaultdict
from typing import NamedTuple
import re

I = None


class TargetPosition(NamedTuple):
    x1: int
    x2: int
    y1: int
    y2: int


class Point(NamedTuple):
    x: int
    y: int


def p1():
    target_pos = parse_input()

    # use equation for sum of naturals
    highest_pos_vel = ((target_pos.y1 + 1) * target_pos.y1 // 2)
    print(highest_pos_vel)


def p2():
    target_pos = parse_input()
    v, n = 0, int((target_pos.x1 * 2) ** 0.5 - 1)  # n-th member of arithmetic progression

    dxs = defaultdict(set)
    for dx_init in range(n, target_pos.x2 + 1):
        x, dx, step = 0, dx_init, 0
        while x <= target_pos.x2 and (dx == 0 and target_pos.x1 <= x or dx != 0):
            x += dx
            if dx > 0: dx -= 1
            step += 1
            if target_pos.x1 <= x <= target_pos.x2:
                dxs[dx_init].add(step)
                if dx == 0:
                    dxs[dx_init] = min(dxs[dx_init])
                    break

    dys = defaultdict(set)
    for dy_init in range(target_pos.y1, -target_pos.y1):
        y, dy, step = 0, dy_init, 0
        while target_pos.y1 <= y:
            y += dy
            dy -= 1
            step += 1
            if target_pos.y1 <= y <= target_pos.y2:
                dys[dy_init].add(step)

    for xsteps in dxs.values():
        for ysteps in dys.values():
            if type(xsteps) is int:
                if xsteps <= max(ysteps):
                    v += 1
            elif xsteps & ysteps:
                v += 1

    print(v)


def parse_input():
    with open('./input') as f:
        text = f.read()

    x_raw = text.split()[2]
    y_raw = text.split()[3]

    regex = '\w=([-0-9]+)\.\.([-0-9]+)'
    x_match = re.match(regex, x_raw)
    y_match = re.match(regex, y_raw)

    x1, x2 = map(int, x_match.groups())
    y1, y2 = map(int, y_match.groups())
    target_pos = TargetPosition(x1, x2, y1, y2)
    return target_pos


if __name__ == '__main__':
    p1()
    p2()
