from collections import namedtuple
from functools import reduce

Point = namedtuple('Point', 'x y')




points = {}
with open('days/3/input') as f:
  lines = f.read().split('\n')
  input_length = len(lines)
  input_width = len(lines[0])
  for i, line in enumerate(lines):
    for j, char in enumerate(line):
      points[Point(j, i)] = char

def get_char_at_coord(coord):
  return points[Point(coord.x % input_width, coord.y)]


def get_trees_for_slope(slope):
    curr_point = Point(0, 0)
    num_trees = 0
    while curr_point.y + 1 < input_length:
      char = get_char_at_coord(curr_point)
      if char == '#':
        num_trees += 1
      curr_point = Point(curr_point.x + slope.x, curr_point.y + slope.y)
    return num_trees


mult = lambda acc, num: acc * num

slopes = [
    Point(1, 1),
    Point(3, 1),
    Point(5, 1),
    Point(7, 1),
    Point(1, 2),
]


print([*map(get_trees_for_slope, slopes)])
print(reduce(mult, map(get_trees_for_slope, slopes)))
