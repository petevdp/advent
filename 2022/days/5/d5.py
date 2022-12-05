from collections import defaultdict
from copy import deepcopy
from typing import NamedTuple


class Move(NamedTuple):
    num: int
    source: int
    dest: int


with open('input') as f:
    stacks_r, moves_r = f.read().split('\n\n')

stacks = defaultdict(list)
for line in stacks_r.split('\n')[::-1][1:]:
    for i in range(0, len(line), 4):
        box_seg = line[i:min(i + 4, len(line))]
        if not box_seg.strip():
            continue
        stacks[(i // 4) + 1].append(box_seg[1])

moves = []
for line in moves_r.strip().split('\n'):
    words = line.split()
    moves.append(Move(int(words[1]), int(words[3]), int(words[-1])))


def p1():
    global stacks
    _stacks = deepcopy(stacks)
    for move in moves:
        for _ in range(move.num):
            _stacks[move.dest].append(_stacks[move.source].pop())
    print("p1:", "".join([s[-1] for s in _stacks.values()]))


def p2():
    global stacks
    _stacks = deepcopy(stacks)
    for move in moves:
        to_move = [_stacks[move.source].pop() for _ in range(move.num)][::-1]
        _stacks[move.dest] += to_move
    print("p2:", "".join([s[-1] for s in _stacks.values()]))


p1()
p2()
