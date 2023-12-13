import re
import itertools
from typing import NamedTuple, Tuple, List, Set
from collections import defaultdict


class PotentialPartNumber(NamedTuple):
    coords: Tuple[int, int]
    id: str


class Part(NamedTuple):
    coords: tuple[int, int]
    char: str


class PartNumber(NamedTuple):
    coords: Tuple[int, int]
    id: str
    adj_parts: Set[Part]


# with open('example_d3.txt') as f:
with open('input_d3.txt') as f:
    lines = f.read().strip().split('\n')


def find_number_indices(input_string):
    pattern = re.compile(r'\d+')
    indices = [(match.start(), match.group()) for match in pattern.finditer(input_string)]
    return indices


nums = [PotentialPartNumber((i, j), id) for i, l in enumerate(lines) for j, id in find_number_indices(l)]

adj_deltas = [*itertools.product([-1, 0, 1], [-1, 0, 1])]


def sum_coords(coords, delta):
    return coords[0] + delta[0], coords[1] + delta[1]


def in_bounds(coords):
    return 0 <= coords[0] < len(lines) and 0 <= coords[1] < len(lines[0])


def to_part_numbers(lines: List[str]):
    pattern = re.compile(r'\d+')
    for i, line in enumerate(lines):
        indices = [(match.start(), match.group()) for match in pattern.finditer(line)]
        for j, id in indices:
            base_coords = i, j
            adj_parts = set()
            for offset in range(len(id)):
                coords = base_coords[0], base_coords[1] + offset
                for d in adj_deltas:
                    adj = sum_coords(coords, d)
                    if not in_bounds(adj):
                        continue
                    char = lines[adj[0]][adj[1]]
                    if re.match(r'[^0-9.]', char) is not None:
                        adj_parts.add(Part(adj, char))

            if len(adj_parts) > 0:
                yield PartNumber(base_coords, id, adj_parts)


part_nums = [*to_part_numbers(lines)]


def p1():
    return sum(int(pn.id) for pn in part_nums)


def p2():
    gear_ratios = defaultdict(lambda: 1)
    gears = defaultdict(lambda: 0)
    for pn in part_nums:
        for part in pn.adj_parts:
            if part.char == '*':
                gear_ratios[part.coords] *= int(pn.id)
                gears[part.coords] += 1

    sum = 0
    for coords, num in gears.items():
        if num != 2:
            continue
        sum += gear_ratios[coords]
    return sum


print(f'p1={p1()}')
print(f'p2={p2()}')
