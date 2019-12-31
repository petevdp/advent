from collections import namedtuple
from pipetools import pipe


def load_input(path="6_universal_orbit_map/input.txt"):
    with open(path, 'r') as f:
        text = f.read()
    return text.splitlines()


def parse_orbits(lines):
    orbits = {}

    for l in lines:
        orbited, orbiting = l.split(')')
        if orbited in orbits:
            orbits[orbited].append(orbiting)
        else:
            orbits[orbited] = [orbiting]
    return orbits


def orbit_checksum(orbits):
    curr_body = 'COM'
    search_stack = [orbits[curr_body]]
    count = 0
    while search_stack:
        curr_search = search_stack[-1]
        if not curr_search:
            search_stack.pop()
            continue

        count += len(search_stack)

        next_search_body = curr_search.pop()

        if next_search_body in orbits:
            search_stack.append(orbits[next_search_body])
    return count


run = pipe | parse_orbits | orbit_checksum | print

lines = load_input()

test = ['COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L']

run(lines)
