def load(location="2_program_alarm/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.split(',')]


reg = load()
# reg = load("2_program_alarm/input2.txt")
print(reg)

for i in range(0, len(reg) - (len(reg) % 4), 4):
    op, inpt1_pos, inpt2_pos, out_pos = reg[i:i+4]
    inpt1 = reg[inpt1_pos]
    inpt2 = reg[inpt2_pos]
    if op == 1:
        reg[out_pos] = inpt1 + inpt2
    elif op == 2:
        reg[out_pos] = inpt1 * inpt2
    elif op == 99:
        break
    else:
        raise Exception(f'unknown op code: {op}')

print(reg[0])
