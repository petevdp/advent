require_relative "./intcode"

def find_max_thruster_signal(program, use_feedback_loop=false)
    settings_range = use_feedback_loop ? 5..9 : 0..4
    possible_phase_settings = settings_range.to_a.permutation.to_a

    max_signal = -Float::INFINITY
    possible_phase_settings.each do |settings|
        circuit = AmplificationCircuit.new(program, settings)
        output = use_feedback_loop ? circuit.run_with_feedback_loop : circuit.run(0)
        max_signal = [output, max_signal].max
    end

    max_signal
end

class AmplificationCircuit
    def initialize(program, phase_settings)
        @program = program
        @amplifiers = phase_settings.map do |s|
            Amplifier.new(@program.dup, s)
        end
    end

    def run(starting_value)
        amplify_cycle starting_value
    end

    def run_with_feedback_loop
        value = 0
        i = 0
        begin
            while true
                value = amplify_cycle value
            end
        rescue AmplifierIsHalted
            value
        end
    end

    private

    def incomplete?
        @amplifiers[-1].incomplete?
    end

    def amplify_cycle(value)
        @amplifiers.inject(value) do |value, amplifier|
            output = amplifier.amplify(value)
        end
    end
end

class Amplifier
    def initialize(program, phase_setting)
        @computer = IntCode.new(program, [phase_setting])
    end

    def amplify(input)
        @computer.inputs.push(input)
        output = @computer.run_until_output_or_halt
        if output == :halted
            raise AmplifierIsHalted
        end

        output
    end

    def complete?
        @computer.halted?
    end
end

class AmplifierIsHalted < StandardError
end