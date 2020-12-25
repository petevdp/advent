from collections import namedtuple
"""
what is the mathematical relationship between lcm(a) + i

.------#------#------#------#------#
-----#-----#-----#-----#-----#-----#

-------------------#-------------------#-------------------#-------------------#-------------------#-------------------#-------------------#-------------------#
-----------------#-----------------#-----------------#-----------------#-----------------#-----------------#-----------------#-----------------#
"""


import sys

filename = sys.argv[1] if len(sys.argv) >= 2 else 'input'
Bus = namedtuple('Bus', 'idx id')

with open(f'days/13/{filename}') as f:
    first, second = f.read().strip().split('\n')
    wait = int(first.strip())
    busses = [Bus(i, int(b)) for i, b in enumerate(second.strip().split(',')) if b != 'x']
    
    
def wait_for_bus(bus):
    return bus - (wait % bus)


checked = [*busses]
i = 1
while i < len(busses):
    curr_bus = checked[i]
    prev_bus = checked[i - 1]
    if prev_bus.id > curr_bus.id:



    

def gcd(a, b):
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a

def gcd_with_offset(a, b, offset):
    while b > 1:
        tmp = b
        b = a % b
        a = tmp
    return a
