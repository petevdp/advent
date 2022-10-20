import sys
from typing import NamedTuple

'''
1 -> 2
2 -> 4
'''


class Coords(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    coord: int
    dir: str


def main():
    all_coords, folds = parse_input()
    for fold in folds:
        all_coords = make_fold(all_coords, fold)
    render(all_coords)


def make_fold(all_coords, fold):
    next_coords = set(all_coords)
    if fold.dir == 'x':
        c_idx = 0
    else:
        c_idx = 1
    for coords in all_coords:
        point_coord = coords[c_idx]
        if point_coord > fold.coord:
            point_coord -= 2 * (point_coord - fold.coord)
            new_coords = [None, None]
            new_coords[c_idx] = point_coord
            new_coords[(c_idx + 1) % 2] = coords[(c_idx + 1) % 2]
            next_coords.remove(coords)
            next_coords.add(Coords(*new_coords))
    return next_coords


def render(coords):
    x_len = max(c.x + 1 for c in coords)
    y_len = max(c.y + 1 for c in coords)

    matrix = [[' ' for _j in range(x_len)] for _i in range(y_len)]

    for i in range(y_len):
        for j in range(x_len):
            if Coords(j, i) in coords:
                matrix[i][j] = '#'
    print('\n'.join([''.join(l) for l in matrix]))


def parse_input(path='./input'):
    with open(path) as f:
        text = f.read().strip()
    dots_raw, folds_raw = text.split('\n\n')

    all_coords = set()
    for dot_raw in dots_raw.split('\n'):
        x, y = map(int, dot_raw.split(','))
        coord = Coords(x, y)
        all_coords.add(coord)

    folds = []
    for line in folds_raw.split('\n'):
        dir, coord = line.split()[-1].split('=')
        folds.append(Fold(int(coord), dir))

    return all_coords, folds


if __name__ == "__main__":
    main()
