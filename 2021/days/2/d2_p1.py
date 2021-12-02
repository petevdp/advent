# %%

def parse_inputs(path="./input"):
    with open(path) as f:
        return [parse_line(l) for l in  f.read().strip().split("\n")]

def parse_line(line):
    instr, value = line.split(" ") 
    return instr, int(value)



I = parse_inputs()

x = 0
y = 0
for instr, value in I:
    if instr == "forward":
        x += value
    if instr == "down":
        y += value
    if instr == "up":
        y -= value
    

print("p1:", x*y)

# %%

x = 0
y = 0
aim = 0
for instr, value in I:
    if instr == "forward":
        x += value
        y += aim * value
    if instr == "down":
        aim += value
    if instr == "up":
        aim -= value
    
print("p2:", x*y)
