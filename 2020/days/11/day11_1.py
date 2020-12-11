from collections import namedtuple
import sys

Coord = namedtuple('Coord', 'x y')
Seat = namedtuple('Seat', 'coord char')


starting_seats = {}

with open('days/11/input') as f:
    for i, line in enumerate(f):
        for j, char in enumerate(line.strip()):
            coord = Coord(j, i)
            starting_seats[coord] = Seat(coord, char)
    
    height = i + 1
    width = j + 1


DELTAS = [
    Coord(1, 0),
    Coord(0, 1),
    Coord(-1, 0),
    Coord(0, -1),
    Coord(1, 1),
    Coord(-1, -1),
    Coord(1, -1),
    Coord(-1, 1),
]

def apply_deltas(coord):
    return [Coord(coord.x + d.x, coord.y + d.y) for d in DELTAS]

def get_adjacent_seats(seats, coord):
    return [seats[c] for c in apply_deltas(coord) if c in seats]

def cycle(prev_seats):
    next_seats = {}
    has_changed = False
    for seat in prev_seats.values():
        
        if seat.char == '.':
            next_seats[seat.coord] = seat
            continue

        adjacent = get_adjacent_seats(prev_seats, seat.coord)
        # print('adj: ', adjacent)
        num_adj_occupied = len([s for s in adjacent if s.char == '#'])
        # print('num: ', num_adj_occupied)
        # print()
        
        if num_adj_occupied == 0:
            char = '#'
        elif num_adj_occupied >= 4:
            char = 'L'
        else:
            char = seat.char
            
        if char != seat.char:
            has_changed = True
        next_seats[seat.coord] = Seat(seat.coord, char)
    return next_seats, has_changed

def display_seats(seats):
    disp_string = ''
    for i in range(height):
        for j in range(width):
            disp_string += seats[Coord(j, i)].char
        disp_string += '\n'
    print(disp_string)

curr_seats = starting_seats
i = 0
while True:
    print('cycle: ', i)
    display_seats(curr_seats)
    next_seats, has_changed = cycle(curr_seats)
    if not has_changed:
        print(len([s for s in next_seats.values() if s.char == '#']))
        sys.exit(1)
    curr_seats = next_seats
    i += 1
    
