def load(location="2_program_alarm/input1.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.split(',')]


starting_reg: list = load()


def try_input(noun, verb, expected_output):
    reg = [starting_reg[0], noun, verb, *starting_reg[3:]]

    for i in range(0, len(reg) - (len(reg) % 4), 4):
        op, inpt1_addr, inpt2_addr, out_addr = reg[i:i+4]
        inpt1 = reg[inpt1_addr]
        inpt2 = reg[inpt2_addr]
        if op == 1:
            reg[out_addr] = inpt1 + inpt2
        elif op == 2:
            reg[out_addr] = inpt1 * inpt2
        elif op == 99:
            break
        else:
            raise Exception(f'unknown op code: {op}')
    out = reg[0]

    return out == expected_output


def find_inputs_with_output(expected_output=19690720):
    for noun in range(100):
        for verb in range(100):
            if try_input(noun, verb, expected_output):
                return noun, verb
    return False


print(find_inputs_with_output())
