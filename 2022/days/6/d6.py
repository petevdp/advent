with open('input') as f:
    stream = f.read().strip()


def earliest_n_unique(n: int):
    for i in range(len(stream)):
        cl = stream[i:i + n]
        if n == len(set(cl)):
            return i + n
    raise "no match found"


print("p1: ", earliest_n_unique(4))
print("p2: ", earliest_n_unique(14))
