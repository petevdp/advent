import math
import itertools


def get_input():
    with open('input') as f:
        for line in f:
            d, v = line.strip().split()
            dist = int(v)
            delta = dist // abs(dist)
            for _ in range(abs(dist)):
                match d:
                    case "U":
                        yield 0, delta
                    case "D":
                        yield 0, -delta
                    case "L":
                        yield -delta, 0
                    case "R":
                        yield delta, 0


def print_rope(rope, size=24):
    board = [["." for _ in range((size * 2) + 1)] for _ in range((size * 2) + 1)]

    def offset(idx):
        return idx + size

    board[offset(0)][offset(0)] = "s"
    for i, seg in reversed([*enumerate(rope)]):
        if i == 0:
            char = "H"
        else:
            char = str(i)
        board[offset(seg[1])][offset(seg[0])] = char

    print("\n".join([*reversed(["".join(r) for r in board])]))


def apply_delta(pos, delta):
    return pos[0] + delta[0], pos[1] + delta[1]


def adjacent(coords):
    for delta in itertools.product((-1, 0, 1), (-1, 0, 1)):
        yield apply_delta(coords, delta)


def sim_segment(head_pos, tail_pos):
    if head_pos == tail_pos or tail_pos in adjacent(head_pos):
        pass
    elif head_pos[0] != tail_pos[0] and head_pos[1] != tail_pos[1]:
        dx = head_pos[0] - tail_pos[0]
        dy = head_pos[1] - tail_pos[1]
        delta = dx // abs(dx), dy // abs(dy)
        tail_pos = apply_delta(tail_pos, delta)
    else:
        for dim, opp_dim in ((0, 1), (1, 0)):
            if head_pos[opp_dim] != tail_pos[opp_dim] or head_pos[dim] == tail_pos[dim]:
                continue
            if head_pos[opp_dim] == tail_pos[opp_dim] and abs(head_pos[dim] - tail_pos[dim]) == 2:
                delta = [0, 0]
                delta_d = head_pos[dim] - tail_pos[dim]
                delta[dim] = delta_d // abs(delta_d)
                tail_pos = apply_delta(tail_pos, delta)
                break
    return tail_pos


rope = [(0, 0) for i in range(10)]
visited_p2 = {(0, 0)}
visited_p1 = {(0, 0)}
# print_rope(rope)
print()
for epoch, move in enumerate(get_input()):
    rope[0] = apply_delta(rope[0], move)
    for i in range(1, len(rope)):
        dt = sim_segment(rope[i - 1], rope[i])
        rope[i] = dt

    visited_p2.add(rope[-1])
    visited_p1.add(rope[1])
    # print(epoch)
    # print_rope(rope)
    # print()

print("p1:", len(visited_p1))
print("p2:", len(visited_p2))
