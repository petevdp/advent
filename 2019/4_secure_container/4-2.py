values = range(256310, 732736 + 1)

num_passing = 0
for v in values:
    digits = [int(d) for d in str(v)]
    if digits != sorted(digits):
        continue

    repeats = {d: 0 for d in set(digits)}

    for d in digits:
        repeats[d] += 1

    for num in repeats.values():
        if num == 2:
            num_passing += 1
            break

print(num_passing)
