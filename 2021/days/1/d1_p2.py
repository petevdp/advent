# %%
def get_input():
    with open("input") as f:
        return [*map(int, f.read().strip().split("\n"))]
    

I = get_input()

def get_window(i):
    return sum(I[i:i+3])


first, *rest = [get_window(i) for i in range(len(I) - 2)]

total = 0
last = first
for l in rest:
    if l > last:
        total += 1
    last = l


print(total)
