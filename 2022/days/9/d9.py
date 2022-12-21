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


def print_rope(size=(6, 6)):
    board = [["." for _ in range(size[0])] for _ in range(size[1])]

    board[0][0] = "s"
    board[tail_pos[1]][tail_pos[0]] = "T"
    board[head_pos[1]][head_pos[0]] = "H"

    print("\n".join([*reversed(["".join(r) for r in board])]))


def apply_delta(pos, delta):
    return pos[0] + delta[0], pos[1] + delta[1]


def adjacent(coords):
    for delta in itertools.product((-1, 0, 1), (-1, 0, 1)):
        yield apply_delta(coords, delta)


tail_pos = head_pos = (0, 0)
visited = {tail_pos}

print(f"{head_pos=}")
for i, move in enumerate(get_input()):
    head_pos = apply_delta(head_pos, move)

    if head_pos == tail_pos or tail_pos in adjacent(head_pos):
        pass
    elif head_pos[0] != tail_pos[0] and head_pos[1] != tail_pos[1]:
        dx = head_pos[0] - tail_pos[0]
        dy = head_pos[1] - tail_pos[1]
        delta = dx // abs(dx), dy // abs(dy)
        tail_pos = apply_delta(tail_pos, delta)
    else:
        for dim, opp_dim in ((0, 1), (1,0)):
            if head_pos[opp_dim] != tail_pos[opp_dim] or head_pos[dim] == tail_pos[dim]:
                continue
            if head_pos[opp_dim] == tail_pos[opp_dim] and abs(head_pos[dim] - tail_pos[dim]) == 2:
                delta = [0, 0]
                delta_d = head_pos[dim] - tail_pos[dim]
                delta[dim] = delta_d // abs(delta_d)
                tail_pos = apply_delta(tail_pos, delta)
                break

    visited.add(tail_pos)
    # print(i)
    # print(f"{move=}")
    # print(f"{head_pos=}")
    # print(f"{tail_pos=}")
    # print_rope()
    # print('\n')


print("p1:", len(visited))
