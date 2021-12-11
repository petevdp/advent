# %%
import numpy as np
from typing import NamedTuple
from itertools import product, count

import re


class Coord(NamedTuple):
    x: int
    y: int


def get_input(path="./input"):
    with open(path) as f:
        return {Coord(j, i): int(n) for i, l in enumerate(f.read().split("\n")) for j, n in enumerate(l)}


ADJ_DELTA = {Coord(i, j) for i, j in product(
    [-1, 0, 1], [-1, 0, 1])} - {Coord(0, 0)}


def get_adj(coord, cells):
    for d in ADJ_DELTA:
        adj = Coord(d.x + coord.x, d.y + coord.y)
        if adj in cells:
            yield adj


def get_cells_to_flash(cells):
    for coord, value in cells.items():
        if value > 9:
            yield coord


def run_step(cells):
    for coord in cells.keys():
        cells[coord] += 1

    flashed_cells = set()
    cells_to_flash = {*get_cells_to_flash(cells)}
    while len(cells_to_flash) > 0:
        flash_coord = cells_to_flash.pop()
        flashed_cells.add(flash_coord)
        for adj in get_adj(flash_coord, cells):
            cells[adj] += 1
            if cells[adj] > 9 and not adj in flashed_cells:
                cells_to_flash.add(adj)

    for coord in flashed_cells:
        cells[coord] = 0

    return flashed_cells


I = get_input()


def part1():
    cells = I.copy()
    flash_count = 0
    for _ in range(100):
        flashed_cells = run_step(cells)
        flash_count += len(flashed_cells)
    return flash_count


def part2():
    cells = I.copy()

    for i in count():
        if sum(cells.values()) > 0:
            run_step(cells)
        else:
            return i


print("p1:", part1())
print("p2:", part2())
