import math


def load(location="3_crossed_wires/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    lines_text = [num for num in text.splitlines()]
    return [*map(lambda l: l.split(','), lines_text)]


def up(start):
    x, y = start
    return (x, y + 1)


def down(start):
    x, y = start
    return (x, y - 1)


def left(start):
    x, y = start
    return (x - 1, y)


def right(start):
    x, y = start
    return (x + 1, y)


dir_update_map = {
    'U': up,
    'D': down,
    'L': left,
    'R': right
}


def get_coords_from_line(line):
    coords = {}
    prev_coord = (0, 0)
    distance = 0
    for inst in line:
        direction = inst[0]
        seg_distance = int(inst[1:])
        segment = []
        for _ in range(1, seg_distance + 1):
            distance += 1
            prev_coord = dir_update_map[direction](prev_coord)
            if prev_coord not in coords:
                coords[prev_coord] = distance
    return coords


def get_min_distance_pair(a, b):
    inter = a.keys() & b.keys()
    min_distance = math.inf
    for coord in inter:
        min_distance = min(min_distance, a[coord] + b[coord])
    return min_distance


lines = load()
a, b = map(get_coords_from_line, lines)

print(get_min_distance_pair(a, b))
