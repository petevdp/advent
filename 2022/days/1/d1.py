with open('input') as f:
    sums = [sum(map(int, e.split())) for e in f.read().split('\n\n')]

print(sum([*sorted(sums, reverse=True)][:3]))
