# %%
from math import prod
from itertools import product, islice
from typing import NamedTuple
from collections import defaultdict


class Coord(NamedTuple):
    x: int
    y: int


def get_input(path="./input"):
    cave_map = {}
    with open(path) as f:
        for i, line in enumerate(f.read().strip().split("\n")):
            for j, num in enumerate(map(int, list(line))):
                cave_map[Coord(j, i)] = num
    return cave_map


I = get_input()

NEIGHBOR_DELTAS = {Coord(1, 0),
                   Coord(-1, 0),
                   Coord(0, 1),
                   Coord(0, -1),
                   }


def get_neighbors(coord):
    for d in NEIGHBOR_DELTAS:
        n_coord = Coord(coord.x - d.x, coord.y - d.y)
        n = I.get(n_coord)
        if n is not None:
            yield n_coord


def get_upstream_neighbors(coord):
    for n_coord in get_neighbors(coord):
        if I[n_coord] > I[coord]:
            yield n_coord


def get_low_points():
    low_points = []
    for coord, num in I.items():
        if len([*get_upstream_neighbors(coord)]) == len([*get_neighbors(coord)]):
            yield coord


def part1():
    return sum([I[p] + 1 for p in get_low_points()])


def part2():
    basin_sizes = []
    for low_point in get_low_points():
        basin_points = set()
        locs_to_check = {low_point}
        while len(locs_to_check) > 0:
            curr = locs_to_check.pop()
            basin_points.add(curr)
            for coord in get_upstream_neighbors(curr):
                if I[coord] == 9 or coord in basin_points:
                    continue
                locs_to_check.add(coord)
        basin_sizes.append(len(basin_points))

    return prod(islice(sorted(basin_sizes, reverse=True), 3))


print("p1: ", part1())
print("p2: ", part2())
