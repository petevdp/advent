from collections import defaultdict
from typing import NamedTuple, List


class Op(NamedTuple):
    code: str
    value: List[int]


def get_input():
    with open("input") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            code, *args = line.split()
            yield Op(code, int(args[0]) if args else None)


sample_cycles = [20, 60, 100, 140, 180, 220]

inputs = get_input()
executing = None
exec_start = None
X = 1
cycle = 1
ans = 0
while True:
    if not executing:
        try:
            executing = next(inputs)
        except StopIteration:
            break
        exec_start = cycle

    if cycle in sample_cycles:
        ans += cycle * X

    if executing.code == "addx" and exec_start == cycle - 1:
        X += executing.value
        executing = None
        exec_start = None
    elif executing.code == "noop":
        executing = None
        exec_start = None
    cycle += 1

print("p1:", ans)
