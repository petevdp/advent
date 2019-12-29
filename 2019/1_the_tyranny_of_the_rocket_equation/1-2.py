def load(location="1_the_tyranny_of_the_rocket_equation/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.splitlines()]


modules = load()
total = 0
for m in modules:
    module_fuel = (m // 3) - 2

    fuel_mass = (module_fuel // 3) - 2
    last_fuel_addition = fuel_mass
    while True:
        last_fuel_addition = (last_fuel_addition // 3) - 2
        if last_fuel_addition > 0:
            fuel_mass += last_fuel_addition
        else:
            break
    total += module_fuel
    total += fuel_mass


print(total)
