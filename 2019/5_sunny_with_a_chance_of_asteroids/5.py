from enum import Enum
from collections import namedtuple


def load_input(location="5_sunny_with_a_chance_of_asteroids/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.split(',')]


class Mode(Enum):
    position = 0
    immediate = 1


class OPCode(Enum):
    add = 1
    multiply = 2
    prompt = 3
    output = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    halt = 99


# mapping from opcodes to number of params
num_params = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0,
}

Param = namedtuple('Param', 'input mode')

Instruction = namedtuple(
    "Instruction",
    "position opcode params"
)


class IntCode:

    def __init__(self, register):
        self.register = register
        self.position = 0

    def run(self):
        while self.position != None:
            instruction = self.parse_instruction(self.position)
            self.execute_instruction(instruction)

    def execute_instruction(self, ins: Instruction):
        if ins.opcode == OPCode.add.value:
            val_a = self.read_param(ins.params[0])
            val_b = self.read_param(ins.params[1])
            result = val_a + val_b
            self.write_param(ins.params[2], result)
            next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.multiply.value:
            val_a = self.read_param(ins.params[0])
            val_b = self.read_param(ins.params[1])
            result = val_a * val_b
            self.write_param(ins.params[2], result)
            next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.prompt.value:
            inpt = int(input("please input something: "))
            self.write_param(ins.params[0], inpt)
            next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.output.value:
            self.output_param(ins.params[0])
            next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.halt.value:
            next_position = None

        elif ins.opcode == OPCode.jump_if_true.value:
            if self.read_param(ins.params[0]) != 0:
                next_position = self.read_param(ins.params[1])
            else:
                next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.jump_if_false.value:
            if self.read_param(ins.params[0]) == 0:
                next_position = self.read_param(ins.params[1])
            else:
                next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.less_than.value:
            a, b = (self.read_param(ins.params[0]),
                    self.read_param(ins.params[1]))

            is_less_than = 1 if a < b else 0
            self.write_param(ins.params[2], is_less_than)
            next_position = self.next_instruction_position(ins)

        elif ins.opcode == OPCode.equals.value:
            a, b = (self.read_param(ins.params[0]),
                    self.read_param(ins.params[1]))
            is_equal = 1 if a == b else 0
            self.write_param(ins.params[2], is_equal)
            next_position = self.next_instruction_position(ins)

        else:
            raise Exception(f'unknown op code: {ins.opcode}')

        self.position = next_position

    def parse_instruction(self, pos):
        op = self.register[pos] % 100  # get last two digits
        inputs = self.register[pos+1:pos+1 + num_params[op]]
        modes = [int(d) for d in str(self.register[pos])[-3::-1]]
        modes += [0] * (num_params[op] - len(modes))
        params = [Param(i, m) for i, m in zip(inputs, modes)]

        return Instruction(pos, op, params)

    def read_param(self, param: Param):
        if param.mode == Mode.immediate.value:
            return param.input

        if param.mode == Mode.position.value:
            return self.register[param.input]

        else:
            raise Exception(f'Mode {param.mode} does not exist.')

    def write_param(self, param, value):
        self.register[param.input] = value

    def output_param(self, param):
        if param.mode == Mode.immediate.value:
            value = param.input

        elif param.mode == Mode.position.value:
            value = self.register[param.input]

        else:
            raise Exception(f'Mode {param.mode} does not exist.')

        print(value)

    """
    get instruction position next to this one
    """

    def next_instruction_position(self, ins):
        return ins.position + len(ins.params) + 1


if __name__ == "__main__":
    input_register = load_input()

    # test programs
    print_pinut = [3, 0, 4, 0, 99]
    multiply = [1002, 4, 3, 4, 33]
    add = [1101, 100, -1, 4, 0]
    is_true_immediate = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    is_true_position = [3, 12, 6, 12, 15, 1,
                        13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    computer = IntCode(input_register)
    computer.run()
