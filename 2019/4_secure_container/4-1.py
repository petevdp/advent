def descending(digits):
    digits == sort(digits, reversed=True)


def repeated(digits):
    return len(digits) > len(set(digits))


# 256310-732736
values = range(256310, 732736 + 1)
# values = [111111, 223450, 123789]

num_passing = 0
for v in values:
    digits = [int(d) for d in str(v)]
    ascending = digits == sorted(digits)
    repeated_nums = len(digits) > len(set(digits))

    if ascending and repeated_nums:
        num_passing += 1

print(num_passing)
