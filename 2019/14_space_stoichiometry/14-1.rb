#!/usr/bin/env ruby

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


i = load_input

c_map = {}

i.each do |m|
    c_map[m[0]] = m[1]
end


req_stack = [{code: "FUEL", num: 1}]
leftover_map = {}
ore_count = 0

while not req_stack.empty?
    req = req_stack.pop
    code = req[:code]
    out_entry = c_map[code]

    num_required = req[:num]
    leftovers = 0
    if leftover_map[code]
        num_required -= leftover_map[code]
        if num_required < 0
            leftovers = num_required.abs
            num_required = 0
        end
    end

    batch_size = out_entry[:num]
    num_batches = (num_required.to_r/batch_size.to_r).ceil
    num_produced = batch_size * num_batches
    leftovers += num_produced - num_required

    leftover_map[code] = leftovers

    new_reqs = out_entry[:inputs].map do |inpt|
        {code: inpt[:code], num: inpt[:num] * num_batches}
    end

    ore, other = new_reqs.partition { |i| i[:code] == "ORE"}

    ore_count += ore.inject(0){ |a, o| a + o[:num] }

    req_stack += other
end

puts "leftovers: #{leftover_map}"
puts "ore: #{ore_count}"