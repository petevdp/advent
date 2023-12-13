def parse():
    # with open('example_d4.txt') as f:
    with open('input_d4.txt') as f:
        lines = [line for line in f.read().strip().split('\n')]
    for line in lines:
        _, idx, *line = line.split()
        idx = int(idx[0])

        winning, ours = [[*map(int, p.strip().split())] for p in " ".join(line).split("|")]
        yield idx, winning, ours


cards = [*parse()]


def p1():
    p1 = 0
    for idx, winning, ours in cards:
        num_matching = sum(n in winning for n in ours)

        if num_matching > 0:
            p1 += 2 ** (num_matching - 1)
    print(f'{p1=}')


def p2():
    scores = [-1] * len(cards)
    for i in range(len(cards)-1, -1, -1):
        _, winning, ours = cards[i]
        num_matching = sum(n in winning for n in ours)
        scores[i] = 1
        scores[i] = sum(scores[i:i+num_matching+1])

    p2 = sum(scores)
    print(f'{p2=}')

p1()
p2()
