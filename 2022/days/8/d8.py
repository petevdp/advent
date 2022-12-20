from itertools import product
import numpy as np

with open('input') as f:
    trees = [[int(t) for t in list(l.strip())] for l in f]

vis_from_top = set()


def get_height(coords):
    x, y = coords
    return trees[y][x]


def remove_nonascending_keys(_list, key_fn):
    prev_max = -1
    for elt in _list:
        if key_fn(elt) > prev_max:
            prev_max = key_fn(elt)
            yield elt


def p1():
    visible = set()
    for xo, yo in [(1, 1), (-1, -1)]:
        coords_y = [*range(len(trees))][::yo]
        coords_x = [*range(len(trees[0]))][::xo]

        for i in coords_y:
            coords = [(j, i) for j in coords_x]
            visible |= set(remove_nonascending_keys(coords, get_height))

        for j in coords_x:
            coords = [(j, i) for i in coords_y]
            visible |= set(remove_nonascending_keys(coords, get_height))

    print("p1: ", len(visible))


def get_num_visible(_list, height):
    for i, t in enumerate(_list):
        if get_height(t) >= height:
            return i + 1
    return len(_list)


def p2():
    max_score = 0
    for x, y in [(j, i) for i in range(len(trees)) for j in range(len(trees[0]))]:
        score = 1
        height = trees[y][x]

        # top
        top = [(x, i) for i in range(y)][::-1]
        score *= get_num_visible(top, height)

        # bottom
        bottom = [(x, i) for i in range(y + 1, len(trees))]
        score *= get_num_visible(bottom, height)

        # left
        left = [(j, y) for j in range(x)][::-1]
        score *= get_num_visible(left, height)

        # right
        right = [(j, y) for j in range(x + 1, len(trees[0]))]
        score *= get_num_visible(right, height)

        max_score = max(max_score, score)

    print("p2:", max_score)


p1()
p2()
