import heapq
import sys


preamble = []
with open('days/9/input') as f:
    all_nums = [int(n) for n in f.read().split()]
    preamble = all_nums[0:25]


def find_num_that_breaks_rule():
    global preamble
    for i in range(25, len(all_nums)):
        target_num = all_nums[i]
        sums = []
        pair_found = False
        for num_a in preamble:
            if target_num - num_a in preamble:
                pair_found = True
                break
        if not pair_found:
            return target_num, i
        preamble = [*preamble[1:], target_num]
    assert False
    


rule_breaking_num, index_of_rule_breaking_num = find_num_that_breaks_rule()


diffs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def distance_from_target(bounds):
    start, end = bounds
    return abs(rule_breaking_num - sum(all_nums[start:end]))

edges_to_try = [(distance_from_target((0, 2)), (0, 2))]
tried = {edges_to_try[0][1]}

cycles = 0
while len(edges_to_try) > 0:
    cycles += 1
    distance, bounds = heapq.heappop(edges_to_try)
    start, end = bounds
    for d_start, d_end in diffs:
        new_start = start + d_start
        new_end = end + d_end
        new_bounds = (new_start, new_end)
        if new_bounds in tried:
            continue
        if new_start >= 0 and new_end < (len(all_nums) + 1):
            distance = distance_from_target(new_bounds)
            if distance == 0:
                print(min(all_nums[new_start:new_end]) + max(all_nums[new_start:new_end]))
                sys.exit(1)
            heapq.heappush(edges_to_try, (distance, new_bounds))
            tried.add(new_bounds)
            

assert False
