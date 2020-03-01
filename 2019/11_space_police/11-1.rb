#!/usr/bin/env ruby
require "set"
require_relative "../IntCodeRuby/intcode"


DIR_MAP = {
    0 => :left,
    1 => :right
}

DIR_CHANGE_MAP = {
    north: {
        left:  :west,
        right: :east
    },
    south: {
        left: :east,
        right: :west
    },
    east: {
        left: :north,
        right: :south
    },
    west: {
        left: :south,
        right: :north
    }
}

CARDINAL_DELTA_MAP = {
    north: [1,0],
    south: [-1,0],
    east: [0,-1],
    west: [0,1],
}

def get_tile_colors(tile_colors={})
    input = load_input
    computer = IntCode.new(input)
    curr_coord = [0,0]
    curr_cardinal = :north
    loop do 
        curr_color = tile_colors[curr_coord] || 0
        computer.inputs.push(curr_color)
        output = computer.run_until_output_or_halt(2)
        if output == :halted
            break
        end

        # set new color
        tile_colors[curr_coord] = output[0]

        # get new coord and cardinal
        direction = DIR_MAP[output[1]]
        curr_cardinal = DIR_CHANGE_MAP[curr_cardinal][direction]

        delta = CARDINAL_DELTA_MAP[curr_cardinal]
        curr_coord = curr_coord.zip(delta).map { |dim_pair| dim_pair.sum }
    end

    tile_colors
end


def load_input(path="./input")
    f = open(path)
    text = f.read
    f.close
    text.split(",").map {|str| str.to_i}
end

if __FILE__ == $0
    puts get_tile_colors.length
end