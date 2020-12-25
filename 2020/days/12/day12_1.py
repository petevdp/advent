from enum import Enum
from collections import namedtuple
import sys
Instr = namedtuple('Instr', 'code value')

input_filename = sys.argv[1] if len(sys.argv) >= 2 else 'input'


instrs  = []
with open(f'days/12/{input_filename}') as f:
    for line in f:
        code =  line.strip()[0]
        value = int(line.strip()[1:])
        instrs.append(Instr(code, value))
        
degrees = 90
pos_x = 0
pos_y = 0
for instr in instrs:
  # instr N means to move north by the given value.
  if instr.code == 'N':
      pos_y += instr.value
  # instr S means to move south by the given value.
  if instr.code == 'S':
      pos_y -= instr.value
  # instr E means to move east by the given value.
  if instr.code == 'E':
      pos_x += instr.value
  # instr W means to move west by the given value.
  if instr.code == 'W':
      pos_x -= instr.value
  # instr L means to turn left the given number of degrees.
  if instr.code == 'L':
      degrees = (degrees - instr.value) % 360
  # instr R means to turn right the given number of degrees.
  if instr.code == 'R':
      degrees = (degrees + instr.value) % 360
  # instr F means to move forward by the given value in the direction the ship is currently facing.
  if instr.code == 'F' and degrees == 0:
      pos_y += instr.value
  if instr.code == 'F' and degrees == 90:
      pos_x += instr.value
  if instr.code == 'F' and degrees == 180:
      pos_y -= instr.value
  if instr.code == 'F' and degrees == 270:
      pos_x -= instr.value


print(abs(pos_x) + abs(pos_y))
