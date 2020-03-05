#!/usr/bin/env ruby

require("gosu")
require_relative("../IntCodeRuby/intcode.rb")


def load_input(path="./input")
  f = File.open(path)
  text = f.read
  f.close
  text.split(",").map{ |c| c.to_i }
end


def run_start_screen(input)

  # input[0] = 2
  c = IntCode.new(input, []) 

  output = c.run_until_output_or_halt(2220)
  puts "output: #{output.length}"

  board = {}

  tile_indexes = (0..(output.length - 1)).step(3)

  tile_indexes.each do |i|
    *coords, code = output[i..(i + 2)]
    board[coords] = code
  end

  board
end

def run_game(input)
  paddle = 16
  ball = 18
  score = nil
  board = {}
  on_input = Proc.new do
    ball <=> paddle
  end
  curr_outputs = []
  on_output = Proc.new do |output|
    curr_outputs.push(output)
    # puts "curr: #{curr_outputs}"
    if curr_outputs.length == 3
      if curr_outputs[0..1] == [-1, 0]
        # puts "score: #{output}"
        score = output
        on_output = []
      end

      case output
      when 3
        paddle = curr_outputs[0]
        # puts "paddle: #{paddle}"
      when 4
        ball = curr_outputs[0]
        # puts "ball: #{ball}"
      end
      curr_outputs = []
    end
  end

  input[0] = 2
  c = IntCode.new(input, [], on_input, on_output)
  c.run
  puts score
end

def select_code(board, code)
  board.entries.select { |coord, c| c == code}
end


def parse_board(output)
  board = {}

  tile_indexes = (0..(output.length - 1)).step(3)

  tile_indexes.each do |i|
    *coords, code = output[i..(i + 2)]
    board[coords] = code
  end

  board
end

def paint_game(board)
  sorted_board = board.keys.sort_by { |c| -c.sum }
  x_max, y_max = sorted_board[0]
  arr_board = []
  x_max += 1
  y_max += 1
  y_max.times.each do |i|
    arr_board.push([])
    x_max.times.each do |j|
      arr_board[i][j] = convert_to_char(board[[j,i]])
    end
  end

  board_s = ""
  arr_board.each do |row|
    board_s += (row.join("") + "\n")
  end
  puts board_s
  puts "y: #{y_max}, x: #{x_max}"
  puts arr_board.length
  puts arr_board[0].length
end

def convert_to_char(mode)
  case mode
  when 0
    " "
  when 1
    "|"
  when 2
    "-"
  when 3
    "_"
  when 4
    "O"
  end
end

run_game(load_input)