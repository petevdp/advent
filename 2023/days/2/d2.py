import re

with open('input_d2.txt') as f:
    # with open('example_d2.txt') as f:
    lines = f.read().strip().split('\n')


def parse_line(l: str):
    match_groups = re.match(r'^Game (\d+): (.+)$', l).groups()
    game = int(match_groups[0])

    groups = []
    for group_raw in match_groups[1].split(";"):
        group = {"red": 0, "blue": 0, "green": 0}
        for k in group_raw.split(","):
            num, color = k.strip().split()
            group[color] = int(num)
        groups.append(group)
    return game, groups


games = [parse_line(l) for l in lines]


def p1():
    def check_game(groups):
        for group in groups:
            if group["red"] > 12 or group["green"] > 13 or group["blue"] > 14:
                return False
        return True

    possible = [id for id, game in games if check_game(game)]
    return sum(possible)


def p2():
    powers = []
    for id, game in games:
        min_possible = {"red": 0, "blue": 0, "green": 0}
        for group in game:
            for color in min_possible.keys():
                min_possible[color] = max(min_possible[color], group[color])

        power = 1
        for color in min_possible.keys():
            power *= min_possible[color]
        powers.append(power)

    return sum(powers)


print(f'p1={p1()}')
print(f'p2={p2()}')
