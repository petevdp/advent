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


def run_orbit_checksum():

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

    run = pipe | parse_orbits | orbit_checksum | print

    lines = load_input()
    run(lines)


def find_direct_parent(orbits, body):
    return next(p for p, orbiting in orbits.items() if body in orbiting)


def path_to_body_from_parent(orbits, parent, body):
    path_to_body = []
    while True:
        if path_to_body:
            direct_parent = find_direct_parent(orbits, path_to_body[-1])
        else:
            direct_parent = find_direct_parent(orbits, body)

        path_to_body.append(direct_parent)
        if path_to_body[-1] == parent:
            break
        if direct_parent == 'COM':
            raise Exception(f'{parent} is not a parent of {body}')
    return path_to_body


def filter_equal(pair):
    a, b = pair
    return a != b


def find_orbital_distance(orbits, a='YOU', b='SAN'):
    a_path = (path_to_body_from_parent(orbits, 'COM', a))
    b_path = set(path_to_body_from_parent(orbits, 'COM', b))
    a_path = set(a_path)

    return len(a_path ^ b_path)


def run_find_orbital_distance():
    inputs = load_input()
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
            'K)L',
            'K)YOU',
            'I)SAN'
            ]

    def find_santa(orbits):
        return find_orbital_distance(orbits, 'YOU', 'SAN')

    run = pipe | parse_orbits | find_santa | print

    run(inputs)


run_find_orbital_distance()
