"""
[*,*,*]
[*,0,*]
[*,*,*]

-1,-1 -> 1, -1
1,-1 -> 1, 1
1,1 -> -1, 1
-1,1 -> -1, -1

0, -1 -> 1, 0
1, 0 -> 0, 1
0, 1 -> -1, 0
-1, 0 -> 0, -1

[1,1,1]
[2,2,2]
[3,3,3]
"""
from collections import defaultdict

import numpy as np
import sparse
import itertools
from dataclasses import dataclass
from typing import NamedTuple, List, Tuple, DefaultDict, Set

FLIPS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
ROTATES = [i for i in range(4)]


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def perm_group_about_0(self):
        '''gets the set of rotations for this coordinate'''
        pass

    def sub_abs(self, to_sub):
        return Coord(
            x=abs(self.x - to_sub.x),
            y=abs(self.y - to_sub.y),
            z=abs(self.z - to_sub.z),
        )

    def add(self, to_sub):
        return Coord(*[elt + to_sub[i] for i, elt in enumerate(self)])

    def compare_key(self):
        val = 0
        for dim_idx in [0, 1, 2]:
            val += self[dim_idx] * (10 ** dim_idx)
        return val

    def orientations(self):
        """output 24 orientations about (0,0,0)"""

        def roll(v):
            return Coord(v[0], v[2], -v[1])

        def turn(v):
            return Coord(-v[1], v[0], v[2])

        for cycle in range(2):
            for step in range(3):  # Yield RTTT 3 times
                self = roll(self)
                yield (self)  # Yield R
                for i in range(3):  # Yield TTT
                    self = turn(self)
                    yield (self)
            self = roll(turn(roll(self)))  # Do RTR

    #
    # def flip(self, flips: Tuple[int, int]):
    #     return Coord(self.x * flips[0], self.y * flips[1])

    # def rotate(self, n):
    #     curr = self
    #     for i in range(n):

    # def compare(self, coord):
    #     return Coord(self.x - coord.x, self.y - coord.y)


class Scanner(NamedTuple):
    name: str
    orig: List[Coord]
    # beacons: np.ndarray
    offset: int
    pair_diffs: DefaultDict[Coord, List[Tuple[int, int]]]
    pair_diff_keys: Set[Coord]

    def match_pair_from_pair_offset(self, pair_offset):
        return self.pair_diffs[pair_offset]



class CoordPair(NamedTuple):
    idmin: int
    idmax: int
    offset: Coord


def get_match_offsets(polycube):
    return [set(idxs) for idxs in polycube.non_zero()]


def main():
    scanners = parse_input()

    to_sort = []
    for curr, scn in itertools.combinations(scanners.values(), 2):
        shared = curr.pair_diff_keys & scn.pair_diff_keys
        num_shared = sum(len(scn.pair_diffs[k]) + len(curr.pair_diffs[k]) for k in shared)
        to_sort.append((curr.name, scn.name, num_shared))

    s_scanner_pairings = sorted(to_sort, key=lambda t: t[2], reverse=True)
    for pair in s_scanner_pairings:
        print(pair)

    while s_scanner_pairings:
        pairing = next(s_scanner_pairings)
        scanner1, scanner2 = scanners[pairing[0]], scanners[pairing[1]]
        shared_offsets = scanner1.pair_diff_keys & scanner2.pair_diff_keys

        curr_offset = next(shared_offsets)
        s1_pairs = scanner1.match_pair_from_pair_offset(curr_offset)
        s2_pairs = scanner2.match_pair_from_pair_offset(curr_offset)


        for s1_p, s2_p in itertools.product(s1_pairs,s2_pairs):
            s1_b1_small = sorted(s1_p[])
            s1_b2_large =
            for idx, s2_ori_b1, s2_ori_b2 in zip(range(24), s2_p[0].orientations(), s2_p[1].orientations()):
                s2_ori_b_small, s2_ori_b_large = sorted((s2_ori_b1, s2_ori_b2), key=Coord.compare_key)



        s2b1_idx, s2b2_idx = next(scanner2.pair_diffs[next()])
        s2b1 = scanner2.orig[s2b1_idx]
        s2b2 = scanner2.orig[s2b2_idx]


        for s2b1o, s2b2o in zip(*(s2b1.orientations(), s2b2.orientations())):
            s2b1_lower, s2b1_higher = sorted((b1o, b20), key=Coord.compare_key)


    glob = s_scanner_pairings[0]




def pair_diffs(beacons: List[Coord]):
    vals = defaultdict(list)
    for b1, b2 in itertools.combinations(enumerate(beacons), 2):
        idx1, b1 = b1
        idx2, b2 = b2
        vals[b1.sub_abs(Coord(*b2))].append((idx1, idx2))
    return vals, set(vals.keys())


def parse_input():
    with open('./input') as f:
        text = f.read().strip()

    store = {}

    for s_raw in text.split('\n\n'):
        name, *beacons_raw = s_raw.strip().split('\n')
        name = name.strip('- ')
        beacons = [[int(d) for d in l.split(',')] for l in beacons_raw]
        beacons = [Coord(*o) for o in beacons]
        store[name] = Scanner(name, beacons, get_offset(beacons), *pair_diffs(beacons))
    return store


def get_offset(beacon_offsets):
    return Coord(
        min(b.x for b in beacon_offsets),
        min(b.y for b in beacon_offsets),
        min(b.z for b in beacon_offsets),
    )


def get_beacons_polycube(beacons_relative):
    min_x = min(b.x for b in beacons_relative)
    max_x = max(b.x for b in beacons_relative) + 1

    min_y = min(b.y for b in beacons_relative)
    max_y = max(b.y for b in beacons_relative) + 1

    min_z = min(b.z for b in beacons_relative)
    max_z = max(b.z for b in beacons_relative) + 1

    offset_coord = (min_x, min_y, min_z)

    coords = [c.sub(offset_coord) for c in beacons_relative]
    shape = max_x - min_x, max_y - min_y, max_z - min_z
    beacons = np.zeros(shape, dtype=np.int8)
    for coord in coords:
        beacons[coord] = 1
    return beacons


def coord_pair_offsets(polycube):
    dims = np.nonzero(polycube)
    coords = zip(*(list(d) for d in dims))
    for c1, c2 in itertools.combinations(coords, 2):
        c1, c2 = Coord(*c1), Coord(*c2)
        cmin, cmax = sorted((c1, c2), key=Coord.compare_key)
        idmin, idmax = polycube[tuple(cmin)], polycube[tuple(cmax)]
        yield cmax.sub(cmin), idmin, idmax


def orientations24(polycube):
    """List all 24 rotations of the given 3d array"""

    def rotations4(polycube, axes):
        """List the four rotations of the given 3d array in the plane spanned by the given axes."""
        for i in range(4):
            yield np.rot90(polycube, i, axes)

    # imagine shape is pointing in axis 0 (up)

    # 4 rotations about axis 0
    yield from rotations4(polycube, (1, 2))

    # rotate 180 about axis 1, now shape is pointing down in axis 0
    # 4 rotations about axis 0
    yield from rotations4(np.rot90(polycube, 2, axes=(0, 2)), (1, 2))

    # rotate 90 or 270 about axis 1, now shape is pointing in axis 2
    # 8 rotations about axis 2
    yield from rotations4(np.rot90(polycube, axes=(0, 2)), (0, 1))
    yield from rotations4(np.rot90(polycube, -1, axes=(0, 2)), (0, 1))

    # rotate about axis 2, now shape is pointing in axis 1
    # 8 rotations about axis 1
    yield from rotations4(np.rot90(polycube, axes=(0, 1)), (0, 2))
    yield from rotations4(np.rot90(polycube, -1, axes=(0, 1)), (0, 2))


# def all_orientations(beacons):
#     """probably inefficient"""
#     orientations = []
#
#     flips = [
#         beacons,  # identity
#         np.flip(beacons, 0),
#         np.flip(beacons, 1),
#         np.flip()
#     ]
#
#     for m in flips:
#         curr = m
#         orientations.append(curr)
#         for i in range(3):
#             curr = curr.rot90()
#             orientations.append(curr)
#
#     to_return = []
#     for ori in orientations:
#         for existing in to_return:
#             if not np.array_equal(ori, existing):
#                 to_return.append(existing)
#     return to_return
#
#
# k
if __name__ == '__main__':
    main()
