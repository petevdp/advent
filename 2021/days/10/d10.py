# %%

def parse_input(path="./input"):
    with open(path) as f:
        return [line for line in f.read().split()]


I = parse_input()

pairs = {
    "(": ")",
    "<": ">",
    "{": "}",
    "[": "]",
}

syntax_error_score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def syntax_score(line):
    stack = []
    for char in line:
        if char in pairs.keys():
            stack.append(char)
        elif pairs[stack[-1]] == char:
            stack.pop()
        else:
            return syntax_error_score_table[char]
    return 0


def part1():
    return sum(syntax_score(line) for line in I)


autocomplate_score_table = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}


def part2():
    scores = []
    for line in I:
        stack = []
        is_malformed = False
        for char in line:
            if char in pairs.keys():
                stack.append(char)
            elif pairs[stack[-1]] == char:
                stack.pop()
            else:
                is_malformed = True
                break

        if not is_malformed and len(stack) > 0:
            score = 0
            for c in stack[::-1]:
                score *= 5
                score += autocomplate_score_table[c]
            scores.append(score)

    scores = sorted(scores)
    return scores[len(scores) // 2]

print("p1:", part1())
print("p2:", part2())
