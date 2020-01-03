require_relative "./intcode"

def find_best_phase_settings(program, starting_input)
    possible_phase_settings = (0..4).to_a.permutation.to_a

    circuit = AmplificationCircuit.new(starting_input, program)

    possible_phase_settings.inject(-Float::INFINITY) do |max_output, settings|
        [circuit.run(settings), max_output].max
    end
end

class AmplificationCircuit
    def initialize(starting_input, program)
        @starting_input = starting_input
        @program = program
    end

    def run phase_settings
        phase_settings.inject(@starting_input) do |input, setting|
            amplify(input, setting)
        end
    end

    private

    def amplify(input, phase_setting)
        amplifier = IntCode.new(@program, [phase_setting, input])
        output = amplifier.run

        if output.length == 1
            return output[0]
        end

        raise "output is the wrong length! #{output}"
    end
end

