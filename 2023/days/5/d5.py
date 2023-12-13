import math
from typing import Set, Tuple
import re
from collections import defaultdict


def parse():
    # with open('input_d5.txt') as f:
    with open('example_d5.txt') as f:
        seeds, *maps_raw = f.read().strip().split("\n\n")
        seeds = [int(s) for s in seeds.split()[1:]]

        title_regex = re.compile(r'(\w+)-to-(\w+) map:')
        maps = {}
        source_index = {}
        dest_index = {}
        for map in maps_raw:
            title, *content = map.strip().split("\n")
            source, destination = title_regex.match(title).groups()
            maps[source, destination] = map = []
            source_index[source] = destination
            dest_index[destination] = source
            for line in content:
                map.append(tuple(int(d) for d in line.strip().split()))
        return seeds, maps, source_index, dest_index


seeds, maps, source_index, dest_index = parse()


def lookup(source, dest, num):
    mapping = maps[source, dest]
    for dest_start, source_start, _range in mapping:
        if source_start <= num < (source_start + _range):
            return dest_start + (num - source_start)
    return num


def lookup_range(source, dest, query_ranges: Set[Tuple[int, int]]):
    """assumes no overlap in mapped ranges"""
    mapping = maps[source, dest]
    query_ranges = {*query_ranges}
    out_ranges = set()
    for dest_start, source_start, mapped_range_len in mapping:
        if not query_ranges:
            break
        query_range = query_ranges.pop()
        modified = False
        source_end = source_start + mapped_range_len

        # does query extend past lower bound?
        if query_range[0] < source_start:
            query_ranges.add((query_range[0], min(query_range[1], source_start)))

        # is there any overlap?
        if source_start < query_range[0]:
            inner_source = source_start, min(source_end, query_range[1])
            offset =  source_start - dest_start
            overlap_range = (inner_source[0] - offset, inner_source[1] - offset)
            out_ranges.add(overlap_range)

        # does query extend past upper bound?
        if query_range[1] > source_start + mapped_range_len:
            query_ranges.add((max(query_range[0], source_end), query_range[1]))


    out_ranges = out_ranges | query_ranges

    return out_ranges


def p1():
    lowest_location_num = math.inf
    stack = [("seed", set(seeds))]
    while stack:
        source, nums = stack[-1]
        if not nums:
            stack.pop()
            continue
        if source == "location":
            lowest_location_num = min(lowest_location_num, *nums)
            stack.pop()
            continue
        dest = source_index[source]
        num = nums.pop()
        dest_num = lookup(source, dest, num)
        stack.append((dest, {dest_num}))

    print(f'p1={lowest_location_num}')


p1()


def p2():
    lowest_location_num = math.inf
    seed_ranges = [(seeds[i], seeds[i + 1] + seeds[i]) for i in range(0, len(seeds), 2)]
    stack = [("seed", set(seed_ranges))]
    while stack:
        print(f'stack: {len(stack)}, {lowest_location_num=}')
        source, ranges = stack[-1]
        if not ranges:
            stack.pop()
            continue
        if source == "location":
            min_lower_bound = min(r[0] for r in ranges)
            lowest_location_num = min(lowest_location_num, min_lower_bound)
            stack.pop()
            continue
        dest = source_index[source]
        dest_ranges = lookup_range(source, dest, {ranges.pop()})
        stack.append((dest, dest_ranges))

    print(f'p2={lowest_location_num}')


p2()
