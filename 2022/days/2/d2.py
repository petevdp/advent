"""
A X rock
B Y paper
C Z scissors
"""


def get_score_p1(round):
    opp, ours = round

    score = {'X': 1, 'Y': 2, 'Z': 3}[ours]

    if round in [('A', 'Y'), ('B', 'Z'), ('C', 'X')]:
        score += 6
    if round in [('A', 'X'), ('B', 'Y'), ('C', 'Z')]:
        score += 3
    if round in [('A', 'Z'), ('B', 'X'), ('C', 'Y')]:
        pass
    return score


def p1():
    print(sum(map(get_score_p1, rounds)))


def get_score_p2(round):
    opp_move, outcome = round
    moves = {
        "X": {"A": 3, "B": 1, "C": 2, },
        "Y": {"A": 1, "B": 2, "C": 3, },
        "Z": {"A": 2, "B": 3, "C": 1, },
    }
    results = {"X": 0, "Y": 3, "Z": 6}
    return moves[outcome][opp_move] + results[outcome]


def p2():
    print(sum(map(get_score_p2, rounds)))


with open('input') as f:
    rounds = [tuple(line.split()) for line in f.read().strip().split('\n')]
    p1()
    p2()
