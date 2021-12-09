# %%
import math
def parse_input(path="input"):
    with open(path) as f:
        return [*map(int, f.read().strip().split(","))]
I = parse_input()

def calc_min_fuel(calc_fuel):
    min_fuel = math.inf
    for pos in range(min(I), max(I) + 1):
        min_fuel_for_pos = calc_fuel(pos)

        if min_fuel_for_pos < min_fuel:
            min_fuel = min_fuel_for_pos
    return min_fuel

def calc_fuel_p1(pos):
    return sum(abs(i - pos) for i in I)


def calc_fuel_p2(pos):
    return sum(sum(range(abs(i - pos) + 1)) for i in I)


print("p1:", calc_min_fuel(calc_fuel_p1))
print("p2:", calc_min_fuel(calc_fuel_p2))

# %%
