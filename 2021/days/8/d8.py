# %%
from itertools import combinations
from collections import defaultdict

import sys

def parse_inputs(path="./input"):
    with open(path) as f:
        for line in  f.read().strip().split('\n'):
            patterns, output = line.split(' | ')
            patterns = [*map(frozenset, patterns.split())]
            output = [*map(frozenset, output.split())]
            yield patterns, output


I = [*parse_inputs()]

DIGIT_PATTERNS = [*map(frozenset, [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg"
])]


def filter_by_segment_count(matching):
    for p, mp in matching:
        yield p, frozenset(dp for dp in mp if len(dp) == len(p))
        
def shared_segment_counts(patterns=DIGIT_PATTERNS):
    segment_counts = defaultdict(lambda: 0)
    for p in patterns:
        for s in p:
            segment_counts[s] += 1
    return segment_counts
        

BASE_SHARED_SEGMENTS = shared_segment_counts()

def segment_counts_for_pattern(pattern, segment_counts):
    counts = defaultdict(lambda: 0)
    for p, c in segment_counts.items():
        if not p in pattern:
            continue
        counts[c] += 1
    return counts


def filter_by_per_segment_counts(matching):
    patterns = [p for p, dp in matching]
    segment_counts = shared_segment_counts(patterns)
    for pattern, matched_digit_patterns in matching:
        segment_counts_for_current_pattern  = segment_counts_for_pattern(pattern, segment_counts)
        still_matching_digit_patterns = set()
        for digit_pattern in matched_digit_patterns:
            segment_counts_for_m = segment_counts_for_pattern(digit_pattern, BASE_SHARED_SEGMENTS)
            if segment_counts_for_m == segment_counts_for_current_pattern:
                still_matching_digit_patterns.add(digit_pattern)
        yield pattern, frozenset(still_matching_digit_patterns)
        
def pattern_to_str(pattern):
    return "".join(sorted(pattern))
    
def print_matches(matches):
    matched_counts = defaultdict(lambda: 0)
    if len(matches) == 0:
        print("no matches") 
    for p, mp in matches:
        for m in mp:
            (DIGIT_PATTERNS.index(m), pattern_to_str(m))
            matched_counts[DIGIT_PATTERNS.index(m)] += 1
            
    for d, c in sorted(matched_counts.items())  :
        print(d,c)

def part1():
    count = 0
    for patterns, output in I:
        matched = [*filter_by_segment_count([(p, DIGIT_PATTERNS) for p in patterns])]
        uniquely_matched_patterns = {p for p, d in matched if len(d) == 1}
        for o in output:
            if o in uniquely_matched_patterns:
                count += 1
                
    return count


def part2():
    total = 0
    rounds = [
        filter_by_segment_count,
        filter_by_per_segment_counts,
    ]
    for patterns, output in I:
        current = [(p, set(DIGIT_PATTERNS)) for p in patterns]
        for round in rounds:
            current = [*round(current)]
            
        if any(len(m) > 1 for p, m in current):
            print("too many matches: ")
            print_matches(current)
            print()
            sys.exit()
            
        pattern_to_dict = {p: DIGIT_PATTERNS.index([*d][0]) for p, d in current}
        num = int("".join([str(pattern_to_dict[o]) for o in output]))
        total += num
    return total 

print("p1: ", part1())
print("p2: ", part2())
