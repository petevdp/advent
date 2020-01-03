from enum import Enum
import math
from collections import namedtuple
from itertools import permutations
from functools import reduce


def load_input(location="7_amplification_circuit/input.txt"):
    with open(location, 'r') as f:
        text: str = f.read()

    return [int(num) for num in text.split(',')]


class Mode(Enum):
    position = 0
    immediate = 1


class OPCode(Enum):
    add = 1
    multiply = 2
    get_input = 3
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

    def __init__(self, register, inputs):
        self.register = register
        self.position = 0
        self.inputs = inputs[:]
        self.output = []

    def run(self):
        while self.position != None:
            instruction = self.parse_instruction(self.position)
            self.execute_instruction(instruction)
        return self.output

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

        elif ins.opcode == OPCode.get_input.value:
            inpt = self.inputs.pop(0)
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

        self.output.append(value)

    def next_instruction_position(self, ins):
        return ins.position + len(ins.params) + 1


class AmplificationCircuit:
    def __init__(self, phase_settings, start_value, program):
        self.program = program
        self.phase_settings = phase_settings
        self.starting_input = start_value

    def run(self):
        return reduce(self.amplify, self.phase_settings, self.starting_input)

    def amplify(self, input_value, phase_setting):
        amplifier = IntCode(self.program, [phase_setting, input_value])
        output = amplifier.run()
        if len(output) != 1:
            raise Exception(f'ouput is the wrong length.. {output}')

        return output[0]


def find_best_phase_settings(program, phase_setting_range):
    possible_phase_settings = [*permutations(phase_setting_range))]
    print(f'checking {len(possible_phase_settings)}possible phase settings')
    max_output = float('-inf')
    max_input_settings = None
    for settings in possible_phase_settings:
        circuit = AmplificationCircuit(settings, 0, program)
        output = circuit.run()
        print(f'output: {output}')
        if output > max_output:
            max_output = output
            max_input_settings = settings

    return max_input_settings, max_output


if __name__ == "__main__":
    input_program = load_input()
    test_program1 = [
3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
    ]

    test_program2 = [
3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
    ]
    print(find_best_phase_settings(input_program, range(5, 10)))
