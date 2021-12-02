# %%
def get_input():
    with open("input") as f:
        return map(int, f.read().strip().split("\n"))
    




first, *rest = get_input()


total = 0
last = first
for l in rest:
    if l > last:
        total += 1
    last = l


print(total)
