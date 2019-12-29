
def load(location="1_the_tyranny_of_the_rocket_equation/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.splitlines()]


modules = load()
sum = 0
for m in modules:
    sum += (m // 3) - 2

print(sum)
