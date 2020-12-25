"""

---
x

-
-
-
 x







"""


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
        
pos_x = 0
pos_y = 0
w_pos_x = 10
w_pos_y = 1
for instr in instrs:

  if instr.code == 'N':
      w_pos_y += instr.value
  if instr.code == 'S':
      w_pos_y -= instr.value
  if instr.code == 'E':
      w_pos_x += instr.value
  if instr.code == 'W':
      w_pos_x -= instr.value
  if instr.code == 'L':
      for _ in range(instr.value // 90):
          w_pos_y, w_pos_x = w_pos_x, w_pos_y * -1
  if instr.code == 'R':
      for _ in range(instr.value // 90):
          w_pos_y, w_pos_x = w_pos_x * -1, w_pos_y
  if instr.code == 'F':
      for i in range(instr.value):
          pos_x += w_pos_x
          pos_y += w_pos_y

print(abs(pos_x) + abs(pos_y))
