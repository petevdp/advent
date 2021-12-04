# %% p1

import numpy as np
import math

def parse_inputs(path="./input"):
    with open(path) as f:
        lines = f.read().strip().split("\n")
        return [[*map(int, list(l))] for l in lines]


I = parse_inputs()

def get_position_mask_gamma(bits):
    half = math.ceil(len(bits) / 2)
    sum_digit = sum(bits)
    gamma = int(sum_digit >= half)
    return bool(gamma)

def get_position_mask_epsilon(bits):
    half = math.ceil(len(bits) / 2)
    sum_digit = sum(bits)
    epsilon = int(sum_digit < half)
    return bool(epsilon)


def b_to_int(b_arr):
    return sum([d* 2**i for i, d in enumerate(reversed(b_arr))])


gamma_bits = [get_position_mask_gamma(bits) for bits in zip(*I)]
epsilon_bits = [not b for b in gamma_bits]

print("p1: ", b_to_int(gamma_bits) * b_to_int(epsilon_bits))

# %% p2


def get_rating(get_mask, nums):
    remaining = nums
    digit_place = 0
    while len(remaining) > 1:
        bits = [d[digit_place] for d in remaining]
        mask = get_mask(bits)
        with_mask = [(b, b[digit_place] == mask) for b in remaining]
        remaining = [b for b in remaining if b[digit_place] == mask]
        digit_place += 1
    
    return b_to_int(remaining[0])


oxygen_rating = get_rating(get_position_mask_gamma, I)
co2_rating = get_rating(get_position_mask_epsilon, I)


print("p2: ", oxygen_rating * co2_rating)
# print("p2: ", oxygen_rating * co2_rating)
