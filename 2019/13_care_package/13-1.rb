#!/usr/bin/env ruby

require_relative("../IntCodeRuby/intcode.rb")

def load_input(path="./input")
  f = File.open(path)
  text = f.read
  f.close
  text.split(",").map{ |c| c.to_i }
end

input = load_input


c = IntCode.new(input) 

output = c.run

board = {}

tile_indexes = (0..(output.length - 1)).step(3)

tile_indexes.each do |i|
  *coords, code = output[i..(i + 2)]
  board[coords] = code
end

puts board.values.(2)
