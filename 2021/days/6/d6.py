# %%
def get_input(path="./input"):
    with open(path) as f:
        return [*map(int, f.read().strip().split(","))]


I = get_input()


def simulate(days):
    children = [0, 0, 0]
    adults = [0 for i in range(0, 7)]
    for f in I:
        adults[f] += 1
    for i in range(0, days):
        child_offset = (i + 7) % 7
        becoming_adults = children[-1]
        for ic, c in enumerate(children[:-1]):
            children[ic + 1] = c
        children[0] = adults[(child_offset) % 7]
        adults[(child_offset - 1) % 7] += becoming_adults

    return sum([*adults, *children])


# %%
print("p1:", simulate(80))
print("p2:", simulate(256))
