require "ruby-enum"

def load_input(location="7_amplification_circuit/input.txt")
    file = File.open(location)
    text = file.read
    file.close

    text
        .split(',')
        .map { |str| str.to_i }
end

class Mode
    include Ruby::Enum

    define :POSITION, 0
    define :IMMEDIATE, 1
end

class OpCode
    include Ruby::Enum

    define :ADD, 1
    define :IMMEDIATE, 2
    define :GET_INPUT, 3
    define :OUTPUT, 4
    define :JUMP_IF_TRUE, 5
    define :JUMP_IF_FALSE, 6
    define :LESS_THAN, 7
    define :EQUALS, 8
    define :HALT, 99
end

# how many paramaters each opcode is expecting
$NUM_PARAMS = {
    1 => 3,
    2 => 3,
    3 => 1,
    4 => 1,
    5 => 2,
    6 => 2,
    7 => 3,
    8 => 3,
    99 => 0,
}

Param = Struct.new(:input, :mode)
Instruction = Struct.new(:position, :opcode, :params)

class IntCode
    attr_reader :register, :outputs, :curr_position

    def initialize(starting_register, inputs)
        @register = starting_register
        @curr_position = 0
        @inputs = inputs
        @outputs = []
    end

    def run
        while @curr_position != nil
            instruction = parse_instruction @curr_position
            @curr_position = execute_instruction instruction
        end
        @outputs
    end

    private

    # execute instruction, and return the next instruction pointer
    def execute_instruction instruction
        puts instruction
        if instruction.opcode == OpCode::ADD
            param_a, param_b, output_location = instruction.params
            value_a = read_param(param_a)
            value_b = read_param(param_b)
            result = value_a + value_b
            write_param(output_location, result)
            return adjacent_instruction instruction
        end

        if instruction.opcode == OpCode::HALT
            return nil
        end

        raise "unknown opcode #opcode"

        @position = next_position
    end

    def parse_instruction position
        code = @register[position]
        opcode = code % 100 # get last two digits
        inputs = @register[position + 1..(position + $NUM_PARAMS[opcode])]

        explicit_str_code = "0" * (inputs.length - (code.to_s.length - 2)) + code.to_s

        modes = explicit_str_code
            # remove last two chars
            .slice(0..-3)
            .chars
            .reverse
            .map {|c| c.to_i}

        params = inputs
            .zip(modes)
            .map { |input, mode| Param.new(input, mode) }

        puts "code: #{code}"
        puts "inputs: #{inputs}"
        puts "modes: #{modes}"
        puts inputs

        i = Instruction.new(position, opcode, params)
        puts "instruction: #{i}"
        i
    end

    def read_param param
        if param.mode == Mode::IMMEDIATE
            return param.input
        end

        if param.mode == Mode::POSITION
            return @register[param.input]
        end

        raise "unknown mode #{param.mode}"

    end

    def write_param location_param, value
        @register[location_param.input] = value
    end

    def adjacent_instruction instruction
        return instruction.position + intruction.params + 1
    end
end