import sys
from collections import deque,defaultdict

input_file = sys.argv[1]

with open(input_file) as f:
    rules_raw, updates_raw = f.read().strip().split('\n\n')
    rules_raw = rules_raw.strip()
    updates_raw = updates_raw.strip()

E_AFTER = defaultdict(set)
E_BEFORE = defaultdict(set)

U = []
for r in rules_raw.split('\n'):
    x,y = map(int,r.split('|'))
    E_AFTER[x].add(y)
    E_BEFORE[y].add(x)

for u_line in updates_raw.split('\n'):
    U.append([*map(int,u_line.strip().split(','))])

p1 = 0
p2 = 0
for upd in U:
    ok = True
    for i in range(len(upd)):
        if E_AFTER[upd[i]] & set(upd[:i]) or E_BEFORE[upd[i]] & set(upd[i+1:]):
            ok = False
            break
    if ok:
        p1 += upd[len(upd) // 2]
        continue

    good = []
    Q = deque()
    LEFT = {v: len(E_BEFORE[v] & set(upd)) for v in upd}
    for v in upd:
        # no values before this one present
        if LEFT[v] == 0:
            Q.append(v)
    while Q:
            x = Q.popleft()
            good.append(x)
            for y in E_AFTER[x]:
                if y not in LEFT:
                    continue
                LEFT[y] -= 1
                if LEFT[y] == 0:
                    Q.append(y)
    p2 += good[len(good)//2]

print('p1', p1)
print('p2', p2)
