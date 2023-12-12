def is_digit(s: str):
    return 48 <= ord(s) <= 57


with open('input_d1.txt') as f:
    # with open('example_d1.txt') as f:
    lines = [l for l in f.read().strip().split("\n")]


def p1():
    sum = 0
    for l in lines:
        digits = [c for c in l if is_digit(c)]
        sum += int(digits[0] + digits[-1])
    return sum


print(f"p1={p1()}")

SPELLED = [
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9"),
    ("zero", "0")
]

SPELLED_BACKWARDS = [(w[::-1], d) for w, d in SPELLED]


def find_first_digit(l, r=False):
    i = 0
    pairs = SPELLED_BACKWARDS if r else SPELLED
    while i < len(l):
        if is_digit(l[i]):
            return l[i]
        for word, digit in pairs:
            if l[i:].startswith(word):
                return digit
        i += 1


def p2():
    sum = 0
    for l in lines:
        first = find_first_digit(l)
        last = find_first_digit(l[::-1], r=True)
        code = first + last
        sum += int(code)
    return sum


print(f"p2={p2()}")
