# %%
from typing import Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Node:
    key: str
    visited_cave_twice: bool
    visited: Set[str]


def parse_input(path="./input"):
    with open(path) as f:
        edges = defaultdict(lambda: set())
        nodes = set()
        for line in f:
            v1, v2 = line.strip().split('-')
            edges[v1].add(v2)
            edges[v2].add(v1)
            nodes.add(v1)
            nodes.add(v2)

        return edges, nodes


EDGES, NODES = parse_input()

paths = []
curr_path = [Node("start", False, set())]
while len(curr_path) > 0:
    node = curr_path[-1]
    if node.key == "end":
        paths.append([n.key for n in curr_path])

    to_visit = EDGES[node.key] - node.visited - {"start"}
    if node.visited_cave_twice:
        to_visit = to_visit - \
            {n.key for n in curr_path if n.key.lower() == n.key}

    if len(to_visit) == 0 or node.key == "end":
        curr_path.pop()
        if len(curr_path) > 0:
            curr_path[-1].visited.add(node.key)
        continue

    for v_key in to_visit:
        visited_cave_twice = node.visited_cave_twice or v_key in {
            pn.key for pn in curr_path if pn.key.lower() == pn.key}
        curr_path.append(Node(v_key, visited_cave_twice, set()))
        break

len(paths)
