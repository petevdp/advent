require "ruby-enum"

class Mode
    include Ruby::Enum
    define :POSITION, 0
    define :IMMEDIATE, 1
    define :RELATIVE, 2
end

class OpCode
    include Ruby::Enum

    define :SUM, 1
    define :PRODUCT, 2
    define :INPUT, 3
    define :OUTPUT, 4
    define :JUMP_IF_TRUE, 5
    define :JUMP_IF_FALSE, 6
    define :LESS_THAN, 7
    define :EQUALS, 8
    define :ADJUST_RELATIVE_BASE, 9
    define :HALT, 99
end

# how many paramaters each opcode is expecting
NUM_PARAMS = {
    1 => 3,
    2 => 3,
    3 => 1,
    4 => 1,
    5 => 2,
    6 => 2,
    7 => 3,
    8 => 3,
    9 => 1,
    99 => 0,
}

Param = Struct.new(:input, :mode)
Instruction = Struct.new(:position, :opcode, :params)

class IntCode
    attr_reader :register, :outputs, :curr_position
    attr_accessor :inputs

    def initialize(starting_register, inputs=[])
        @register = starting_register.dup
        @curr_position = 0
        @inputs = inputs.dup
        @outputs = []
        @relative_base = 0
    end

    def run
        if halted?
            raise ProgramIsHaltedError
        end

        while !halted?
            instruction = parse_instruction @curr_position
            @curr_position = execute_instruction instruction
        end

        @outputs
    end

    def run_until_output_or_halt(num_expected_outputs=1)
        if halted?
            raise ProgramIsHaltedError
        end

        while (!halted?) && (@outputs.length < num_expected_outputs)
            instruction = parse_instruction(@curr_position)
            @curr_position = execute_instruction instruction
        end

        # either return the output or nil if none was provided

        if halted?
            return :halted
        end

        if outputs.empty?
            raise "something went wrong with the while loop"
        end

        @outputs.pop(num_expected_outputs)
    end

    def halted?
        @curr_position == nil
    end

    private

    # execute instruction, and return the next instruction pointer
    def execute_instruction instruction
        case instruction.opcode
        when OpCode::SUM
            param_a, param_b, output_location = instruction.params
            value_a = read_param(param_a)
            value_b = read_param(param_b)
            result = value_a + value_b
            write_param(output_location, result)

            return adjacent_instruction_position instruction

        when OpCode::PRODUCT
            param_a, param_b, write_location = instruction.params
            value_a = read_param(param_a)
            value_b = read_param(param_b)
            result = value_a * value_b
            write_param(write_location, result)

            return adjacent_instruction_position instruction

        when OpCode::INPUT
            if @inputs.empty?
                raise "inputs is empty!"
            end
            input = @inputs.shift()
            write_location = instruction.params[0]
            write_param(write_location, input)

            return adjacent_instruction_position instruction

        when OpCode::OUTPUT
            output_param(instruction.params[0])
            return adjacent_instruction_position instruction

        when OpCode::JUMP_IF_TRUE
            predicate_param, position_to_jump_to = instruction.params

            if read_param(predicate_param) != 0
                return read_param(position_to_jump_to)
            end

            return adjacent_instruction_position instruction

        when OpCode::JUMP_IF_FALSE
            predicate_param, position_to_jump_to = instruction.params

            if read_param(predicate_param) == 0
                return read_param(position_to_jump_to)
            end

            return adjacent_instruction_position instruction

        when OpCode::LESS_THAN
            param_a, param_b, write_position = instruction.params
            a, b = [param_a, param_b].map { |p| read_param(p) }
            result = a < b ? 1 : 0
            write_param(write_position, result)

            return adjacent_instruction_position instruction

        when OpCode::EQUALS
            param_a, param_b, write_position = instruction.params
            a, b = [param_a, param_b].map { |p| read_param(p) }
            result = a == b ? 1 : 0
            write_param(write_position, result)

            return adjacent_instruction_position instruction

        when OpCode::ADJUST_RELATIVE_BASE
            param = instruction.params[0]
            @relative_base += read_param(param)

            return adjacent_instruction_position instruction

        when OpCode::HALT
            return nil
        end

        raise "unknown opcode #{opcode}"
    end

    def parse_instruction position
        puts "position: #{position}"
        code = @register[position]
        opcode = code % 100 # get last two digits
        puts "opcode: #{opcode}"
        puts opcode.class
        puts NUM_PARAMS[opcode]
        instruction_range = (position + 1)..(position + NUM_PARAMS[opcode])
        inputs = instruction_range.map do |i|
            # check for a value at that position, else give zero
            @register[i] || 0
        end

        # append implicit 0s to left
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

        Instruction.new(position, opcode, params)
    end

    def read_param param
        if param.mode == Mode::IMMEDIATE
            return param.input
        end

        if param.mode == Mode::POSITION
            value = @register[param.input]
        elsif param.mode == Mode::RELATIVE
            value = @register[@relative_base + param.input]
        else
            raise "unknown mode #{param.mode}"
        end

        value || 0
    end

    def write_param location_param, value
        case location_param.mode
        when Mode::RELATIVE
            input = @relative_base + location_param.input
        when Mode::POSITION
            input = location_param.input
        else
            raise "unsupported mode #{location_param.mode} for writing"
        end

        @register[input] = value
    end

    def output_param param
        if param.mode == Mode::IMMEDIATE
            value = param.input
        elsif param.mode == Mode::POSITION
            value = @register[param.input]
        elsif param.mode == Mode::RELATIVE
            value = @register[@relative_base + param.input]
        else
            raise "mode #{param.mode} does not exist"
        end

        @outputs.append(value)
    end

    # get the position of the next instruction to the left
    def adjacent_instruction_position instruction
        return instruction.position + instruction.params.length + 1
    end

end

class ProgramIsHaltedError < StandardError
end