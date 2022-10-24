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


target_pos: TargetPosition = None




def p1():
    global target_pos
    target_pos = parse_input()

    highest_pos_vel = ((target_pos.y1 + 1) * target_pos.y1 // 2)
    print(highest_pos_vel)


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
