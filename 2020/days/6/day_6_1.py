import re

groups = []
with open('days/6/input') as f:
    for str_group in f.read().split('\n\n'):
        group = set(re.sub('\s', '', str_group))
        groups.append(group)
        

print(sum(len(g) for g in groups))
