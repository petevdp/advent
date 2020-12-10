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
            return target_num
        preamble = [*preamble[1:], target_num]
    assert False
    


rule_breaking_num = find_num_that_breaks_rule()
print(rule_breaking_num)
