import re
from collections import defaultdict

with open('input') as f:
    lines = f.read().strip().split('\n')

dir_filesizes = defaultdict(lambda: 0)

curr_path = ["/"]


def add_size_to_path(size):
    for i in range(1, len(curr_path) + 1):
        dir_filesizes['/'.join(curr_path[:i])] += size


for line in lines:
    if line.startswith("$ cd"):
        path = line.split()[2]
        if path == "..":
            curr_path.pop()
        elif path == '/':
            curr_path = ["/"]
        else:
            curr_path.append(path)
    elif re.match(r"^\d+ ", line):
        add_size_to_path(int(line.split()[0]))

# p1
sizes = [size for size in dir_filesizes.values() if size <= 100_000]
print("p1: ", sum(sizes))

total_used = dir_filesizes["/"]

min_delete = abs(70_000_000 - total_used - 30000000)

# p2
for size in sorted(dir_filesizes.values()):
    if size >= min_delete:
        break

print("p2: ", size)
