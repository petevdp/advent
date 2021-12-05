# %%
import math
import re
from collections import namedtuple 



Point = namedtuple("Point", "x y")
Line = namedtuple("Line", "x1 y1 x2 y2")

def parse_inputs(path="input"):
    with open(path) as f:
        text = f.read()
    
    return [parse_line(line) for line in text.strip().split("\n")]
    

# 644,38 -> 644,265
def parse_line(line):
    return Line(*map(int, re.match("(\d+),(\d+) -> (\d+),(\d+)", line).groups()))


def is_vertical(line):
    return line.x1 == line.x2

def is_horizontal(line):
    return line.y1 == line.y2

def is_straight(line):
    return is_vertical(line) or is_horizontal(line)

def plot_line(line):
    min_y, max_y = sorted((line.y1, line.y2))
    min_x, max_x = sorted((line.x1, line.x2))
    if is_vertical(line):
        return [Point(line.x1, y) for y in  range(min_y, max_y + 1)]
    if is_horizontal(line):
        return [Point(x, line.y1) for x in  range(min_x, max_x + 1)]

    dx = line.x2 - line.x1
    dy = line.y2 - line.y1
    

    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    
    range_x = range(line.x1, line.x1 + dx + step_x, step_x)
    range_y = range(line.y1, line.y1 + dy + step_y, step_y)

    return [Point(x,y) for x,y in zip(range_x, range_y)]
    

lines = parse_inputs()

points = [point for line in lines for point in plot_line(line)]
occupied = set()
overlapping = set()
for point in points:
    if point in occupied:
        overlapping.add(point)
    occupied.add(point)

len(overlapping)



# %%
