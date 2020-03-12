#!/usr/bin/env ruby
require_relative("../IntCodeRuby/intcode")
=begin
ASCII code: 35 means #, 46 means ., 10 starts a new line of output below the current one, and so on. (Within a line, characters are drawn left-to-right.)
=end

ASCII_MAP = {
    35 => "#",
    46 => ".",
    10 => "\n"
}

ADJ_DELTAS = [
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1],
]

def main
    computer = IntCode.new(load_input)
    output = computer.run
    puts paint_scaffold(output)
    coords =  build_coord_map(output)
    intersection_entries = coords.entries.select do |c,t|
        x,y = c
        if t != 35
            next false
        end
        # puts "coord: #{c}, type: #{t}"
        ADJ_DELTAS
            .map {|d| [d[0] + x, d[1] + y] }
            .all? { |c| coords[c] == 35 }
    end

    res = intersection_entries
        .map { |e| e[0] }
        .inject(0) { |s, c| s + (c[0] * c[1]) }

    puts res
end

def build_coord_map(output)
    x, y = [0,0]
    coord_map = {}
    output.each do |o|
        if o == 10
            x, y = [0, y + 1]
        else
            coord_map[[x,y]] = o
            x += 1
        end
    end
    coord_map
end

def paint_scaffold(output)
    text = ""
    output.each do |o|
        text += o.chr
    end
    text
end

def load_input(path="./input")
    f = File.open(path)
    text = f.read
    f.close
    text.split(",").map(&:to_i)
end

if __FILE__ == $0
    main
end