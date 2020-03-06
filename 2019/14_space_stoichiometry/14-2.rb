#!/usr/bin/env ruby
require "json"

def main
    input = load_input

    reactions = {}
    input.each do |m|
        reactions[m[0]] = m[1]
    end


    ore_count = 1000000000000

    upper = ore_count
    lower = 0

    while lower < upper
        mid = ((upper - lower) / 2) + lower
        ore_consumed = produce_fuel(reactions, mid)
        if ore_consumed == ore_count
            return mid
        elsif ore_consumed > ore_count
            upper = mid 
        else
            lower = mid + 1
        end
        puts "upper: #{upper}, lower: #{lower}, mid: #{mid}, consumed: #{ore_consumed}"
    end
    puts "end: #{mid}"
end

def produce_fuel(reactions, fuel_to_produce)
    leftover_map = {}
    ore_used = 0
    reactions.keys.each { |k| leftover_map[k] = 0 }
    req_stack = [{code: "FUEL", num: fuel_to_produce}]
    while not req_stack.empty?
        # puts "reqs: #{req_stack}"
        req = req_stack.pop
        code = req[:code]
        reaction = reactions[code]

        # num_leftover = leftover_map[code] || 0
        num_required = req[:num]
        leftovers = 0
        if leftover_map[code]
            num_required -= leftover_map[code]
            if num_required < 0
                leftovers = num_required.abs
                num_required = 0
            end
        end

        batch_size = reaction[:num]
        num_batches = (num_required.to_r/batch_size.to_r).ceil
        num_produced = batch_size * num_batches
        leftovers += num_produced - num_required

        leftover_map[code] = leftovers

        new_reqs = reaction[:inputs].map do |inpt|
            {code: inpt[:code], num: inpt[:num] * num_batches}
        end

        ore, other = new_reqs.partition { |r| r[:code] == "ORE"}

        ore_used += ore.inject(0){ |a, o| a + o[:num] }
        req_stack += other
        # puts "batches: #{batch_size}"
        # puts "stack"
        # puts req_stack
        # puts "leftovers"
        # puts leftover_map
        # puts "ore count: #{ore_count}"
        # puts
    end
    ore_used
end


def load_input(path="./input")
    f = File.open(path)
    lines = f.read.split("\n")
    f.close
    lines.map{ |l| parse_reaction(l) }
end


def parse_reaction(line)
    inputs, output = line.split("=>")

    output = parse_chemical(output)
    inputs = inputs.split(",").map {|i| parse_chemical(i)}

    [output[:code], {num: output[:num], inputs: inputs}]
end

def parse_chemical(text)
    num, code = text.strip.split

    {num: num.to_i, code: code}
end

def hash_key hash
    hash.entries
        .sort_by {|e| e[0]}
        .map {|e| e[1]}
        .join("")
end

if __FILE__ == $0
    puts main
end