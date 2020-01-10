#!/usr/bin/env ruby

require_relative "amplification_circuit"
require_relative "intcode"

def load_input(day)
    file = File.open("./inputs/#{day}")
    text = file.read
    file.close

    text
        .split(',')
        .map { |str| str.to_i }
end


if __FILE__ == $0
    problem = ARGV[0]
    day = problem[0]
    input = load_input(day)

    case problem
    when '7-1'
        result = find_max_thruster_signal(input)
    when '7-2'
        result = find_max_thruster_signal(input, true) #turn on feedback loop
    when '9-1'
        computer = IntCode.new(input, [1])
        computer.run
        result = computer.outputs
    when '9-2'
        computer = IntCode.new(input, [2])
        computer.run
        result = computer.outputs
    else
        raise "invalid problem #{problem}"
    end

    puts "result: #{result}"
end