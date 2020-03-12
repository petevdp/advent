#!/usr/bin/env ruby

require "set"
def load_input(path="./input")
    f = File.open(path)
    text = f.read
    f.close

    (text.strip.split("").map(&:to_i) * 10000)
end
arr = load_input
base_pattern = [0, 1, 0, -1]
offset = arr[0..6].join("").to_i
code_range = (offset + 1)..(offset + 8)

affected_range = (offset)..(arr.length - 1)
affected_arr = arr[affected_range]

100.times.each do |iter|
    total = 0
    affected_arr = (0..(affected_arr.to_a.length - 1)).map do |index|
        if index == 0
            total = affected_arr.sum
        else
            total -= affected_arr[index-1]
        end
        total.abs % 10
    end
    puts "iter: #{iter}"
end

puts "code: #{affected_arr[0..7].join("")}"