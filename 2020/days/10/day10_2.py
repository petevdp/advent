with open('days/10/input') as f:
    adapters = [int(n) for n in f.read().strip().split('\n')]
    
s_adapters = [0, *sorted(adapters), max(adapters) + 3]
adapters_set = set(s_adapters)
mults = {0: 1}

for num in s_adapters[1:]:
    mults[num] = sum(mults[n] for n in [num - 1, num - 2, num - 3] if n in adapters_set)


print(mults[s_adapters[-1]])
