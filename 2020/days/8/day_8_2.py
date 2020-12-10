from collections import namedtuple

Inst = namedtuple('Inst', 'op num')



starting_insts = []
def main():
    with open('days/8/input') as f:
        for line in f:
            op, num_str = line.strip().split(' ')
            starting_insts.append(Inst(op, int(num_str)))


    index_to_change = find_index_to_change()

    program_to_run = []
    for i, inst in enumerate(starting_insts):
        if i == index_to_change:
            if inst.op == 'jmp':
                opcode = 'nop'
            if inst.op == 'nop':
                opcode = 'jmp'
            program_to_run.append(Inst(opcode, inst.num))
        else:
            program_to_run.append(inst)
            
            
    print(will_terminate_from_instruction(0, program_to_run))


def find_index_to_change():
    good_paths = set()
    _, base_visited = will_terminate_from_instruction(0, starting_insts)
    for index in range(len(starting_insts)):
        if not will_terminate_from_instruction(index, starting_insts)[0] == None:
            good_paths.add(index)
            

    for index in [i for i in base_visited if starting_insts[i].op == 'jmp']:
        if index + 1 in good_paths:
            return index

    for index in [i for i in base_visited if starting_insts[i].op == 'nop']:
        if index + starting_insts[index].num in good_paths:
            return index

    assert False


def will_terminate_from_instruction(index, insts):
    acc = 0
    visited = set()
    curr_index = index
    while not curr_index in visited:
        visited.add(curr_index)
        inst = insts[curr_index]
        if inst.op == 'acc':
            acc += inst.num
            curr_index += 1
        elif inst.op == 'jmp':
            curr_index += inst.num
        else:
            curr_index += 1
        if curr_index == len(insts):
            return acc, visited
    return None, visited


if __name__ == '__main__':
    main()
