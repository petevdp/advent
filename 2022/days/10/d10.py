from collections import defaultdict
from typing import NamedTuple, List


class Op(NamedTuple):
    code: str
    value: List[int]


def get_input():
    with open("example") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            code, *args = line.split()
            yield Op(code, int(args[0]) if args else None)


sample_cycles = [20, 60, 100, 140, 180, 220]
pixels = []

inputs = get_input()
executing = None
exec_start = None
X = 1
cycle = 1
ans_p1 = 0


def sprite_pos():
    if X == 39:
        return X - 1, X
    if X == 40:
        return X, X + 1
    return X - 1, X, X + 1


while True:
    if not executing:
        try:
            executing = next(inputs)
        except StopIteration:
            break
        exec_start = cycle

    if cycle in sample_cycles:
        ans_p1 += cycle * X

    if executing.code == "addx" and exec_start == cycle - 1:
        X += executing.value
        executing = None
        exec_start = None
    elif executing.code == "noop":
        executing = None
        exec_start = None
    pixels.append(cycle in sprite_pos())
    cycle += 1

print("p1:", ans_p1)

image = ""
for i, draw in enumerate(pixels):
    image += "#" if draw else "."
    if (i + 1) % 40 == 0:
        image += "\n"
print(image)
print("--end--")
