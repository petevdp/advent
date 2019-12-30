def load(location="3_crossed_wires/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    lines_text = [num for num in text.splitlines()]
    return [*map(lambda l: l.split(','), lines_text)]


def up(d, start):
    x, y = start
    return [(x, y + i) for i in range(1, d + 1)]


def down(d, start):
    x, y = start
    return [(x, y - i) for i in range(1, d + 1)]


def left(d, start):
    x, y = start
    return [(x - i, y) for i in range(1, d + 1)]


def right(d, start):
    x, y = start
    return [(x + i, y) for i in range(1, d + 1)]


dir_update_map = {
    'U': up,
    'D': down,
    'L': left,
    'R': right
}


def get_coords_from_line(line):
    coords = set()
    prev_coord = (0, 0)
    for inst in line:
        dir = inst[0]
        dist = int(inst[1:])
        segment = dir_update_map[dir](dist, prev_coord)
        prev_coord = segment[-1]
        coords = coords | {c for c in segment}
    return coords


def manhatten_dist(coords):
    x, y = coords
    return abs(x) + abs(y)


def get_closest_coord_pair(a, b):
    inter = a & b
    return min(map(manhatten_dist, inter))


lines = load()
a, b = map(get_coords_from_line, lines)

print(get_closest_coord_pair(a, b))
