from collections import Counter


def main():
    template, rule_graph = parse_input()
    solution_dp(template, rule_graph, 40)


def solution_dp(template, rule_graph, depth):
    prev_depth_counts = {}

    def default_counter(ins):
        return Counter([(ins, 1)])

    for r in rule_graph.keys():
        prev_depth_counts[r] = default_counter(rule_graph[r])
    for g in range(depth - 1):
        curr_depth_counts = {}
        for pattern in rule_graph.keys():
            insert = rule_graph[pattern]
            left = pattern[0] + insert
            right = insert + pattern[1]
            left_counts = prev_depth_counts.get(left, Counter())
            right_counts = prev_depth_counts.get(right, Counter())
            curr_depth_counts[pattern] = left_counts + right_counts + default_counter(insert)
        prev_depth_counts = curr_depth_counts

    total_counts = Counter([(c, 1) for c in template])
    for s1, s2 in zip(template[:-1], template[1:]):
        pattern = s1 + s2
        if pattern in curr_depth_counts:
            total_counts += curr_depth_counts[pattern]

    print(total_counts)
    max_char = max(total_counts.keys(), key=lambda c: total_counts[c])
    min_char = min(total_counts.keys(), key=lambda c: total_counts[c])
    max_char_count = total_counts[max_char]
    min_char_count = total_counts[min_char]
    max_min_diff = max_char_count - min_char_count
    print(f'{max_char=} {max_char_count=} {min_char=} {min_char_count=}')
    print(f'ans: {max_min_diff}')


def parse_input(path='./input'):
    with open(path) as f:
        text = f.read().strip()

    template, rules = text.split('\n\n')
    template = template.strip()
    parsed_rules = {}
    for rule in rules.strip().split('\n'):
        pair, insert = rule.split(' -> ')
        parsed_rules[pair] = insert
    return template, parsed_rules


if __name__ == '__main__':
    main()
