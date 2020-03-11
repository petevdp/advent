#!/usr/bin/env ruby
test_0 = ["12345678"]
test_1 = ["80871224585914546619083218645595", "24176176"]
test_2 = ["19617804207202209144916044189917", "73745418"]

def load_input(path="./input")
    f = File.open(path)
    text = f.read
    f.close

    text.strip.split("").map(&:to_i)
end

arr = load_input
base_pattern = [0, 1, 0, -1]

100.times.each do |i|
    new_arr = arr.each_with_index.map do |elt, index|
        compare_pattern = base_pattern
            .map {|n| [n] * (index+1)}
            .flatten


        new_elt = arr.each_with_index.map do |e, i|
            comp = (e * compare_pattern[((i + 1) % compare_pattern.length)])
            # puts "#{e} * #{compare_pattern[((i + 1) % compare_pattern.length)]} = #{comp}"
            comp
        end.sum.abs % 10

        # puts "index: #{index}"
        # puts "compare: #{compare_pattern}"
        # puts "new_elt: #{new_elt}"
        new_elt
    end
    arr = new_arr
end

puts arr[0..7].join("")