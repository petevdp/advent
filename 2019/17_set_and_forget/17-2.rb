#!/usr/bin/env ruby
# frozen_string_literal: true

require "set"
require_relative('../IntCodeRuby/intcode')

ASCII_MAP = {
  35 => '#',
  46 => '.',
  10 => "\n"
}.freeze

ADJ_DELTAS = [
  [-1, 0],
  [1, 0],
  [0, -1],
  [0, 1]
].freeze

CARDINALS = {
  north: [0, -1],
  south: [0, 1],
  east: [1, 0],
  west: [-1, 0]
}.freeze

ORIENTATIONS = {
  north: {
    forward: :north,
    left: :west,
    right: :east
  },
  south: {
    forward: :south,
    left: :east,
    right: :west
  },
  east: {
    forward: :east,
    left: :north,
    right: :south
  },
  west: {
    forward: :west,
    left: :south,
    right: :north
  }
}.freeze

def main
  program = load_input
  paint_computer = IntCode.new(program)
  output = paint_computer.run
  coords = build_coord_map(output)
  intersection_entries = coords.entries.select do |c, t|
    x, y = c
    next false if t != '#'

    ADJ_DELTAS
      .map { |d| [d[0] + x, d[1] + y] }
      .all? { |c| coords[c] == '#' }
  end

  res = intersection_entries
        .map { |e| e[0] }
        .inject(0) { |s, c| s + (c[0] * c[1]) }

  full_path = walk_path(coords).join("")
  puts paint_scaffold(output)
  turn_seq = get_turn_sequence(full_path)
  puts turn_seq
  all_subeqs = all_turn_subsequences(turn_seq)
  puts all_subeqs
  return
  sequence = find_main_sequence(full_path)
  puts "sequence: #{sequence.to_s}"
  funcs = sequence_to_funcs(sequence)
  inputs = funcs_to_input(funcs)

  output[0] = 2
  solve_computer = IntCode.new(program)
  puts solve_computer.run
end

def walk_path(coord_map)
  curr_coord = get_starting_coord(coord_map)
  curr_orientation = :north
  path_walked = []
  loop do
    changes = get_changes(curr_orientation, curr_coord)
    if coord_map[changes[:forward]] == '#'
      curr_coord = changes[:forward] 
      path_walked.push("F")
    elsif coord_map[changes[:left]] == '#'
      curr_orientation = ORIENTATIONS[curr_orientation][:left]
      path_walked.push('L')
    elsif coord_map[changes[:right]] == '#'
      curr_orientation = ORIENTATIONS[curr_orientation][:right]
      path_walked.push('R')
    else
      break
    end
  end
  path_walked
end

def all_turn_subsequences(sequence)
  sub_seqs = Set[]
  sequence.length.times.each do |start|
    (1..(sequence.length - 1)).each do |last|
      sub_seqs.add(sequence[start..last])
    end
  end
  sub_seqs
end

def get_turn_sequence(full_path)
  full_path.tr('F', '')
end

def find_main_sequence(full_path)
  all_indexes = Set[*(0..(full_path.length - 1))]
  subs = {}
  (1..15).each do |i|
    puts ("finding for #{i}")
    subs_for_l = find_substrings_of_length(full_path, i)
    inter = subs.keys.intersection(subs_for_l.keys)
    subs.merge!(subs_for_l)
  end
  subs.keys
    .select { |s| char_cost(s) <= 20 }
    .combination(3)
    .select do |arr|
      touched_keys = arr.inject(Set[]) { |acc, str| acc +  subs[str]}
      if touched_keys != all_indexes
        next false
      end

      touched_keys == all_indexes
    end
    .sort_by { |funcs|  - funcs.inject(0) { |sum, str| sum + str.length } }
    .map { |funcs| apply_funcs_to_path(full_path, funcs) }
    .inject([]) { |acc, sequences| acc + sequences }
    .sort_by { |seq| seq.length }[0]
end

def sequence_to_funcs(full_sequence)
  movement_seqs = Set[*full_sequence].to_a
  puts "full: #{full_sequence}"
  main_seq = full_sequence.map do |seq|
    puts "inner: #{seq}"
    (movement_seqs.index(seq) + 1)
  end.join(",")
  movement_funcs = movement_seqs.map do |seq|
    seq.gsub(/F+/) { |sub| sub.length }
  end
  [main_seq, *movement_funcs]
end

def funcs_to_input(funcs)
  [*funcs, "n"]
    .map do |f|
      f
        .split("")
        .join(",")
    end
    .join("\n")
    .split("")
    .map(&:ord)
end

def apply_funcs_to_path(path, funcs)
  funcs = Set[*funcs]
  main_funcs = []
  stack = [[0, []]]
  end_sets = Set[]
  while not stack.empty?
    index, tried = stack[-1]
    compatible_funcs = funcs.select { |f| f == path[index, f.length] }
    untried = Set[*compatible_funcs] - Set[*tried]
    if untried.length == 0
      end_sets.add(index)
      func_sequence = stack
        .map {|elt| elt[1][-1]}
      

      built_path = func_sequence.join('')
      if built_path == path
        puts "found seq len: #{func_sequence.length}, #{func_sequence}"
        main_funcs.push(func_sequence)
      end

      stack.pop
      next
    end
    to_try = untried.to_a[-1]
    new_index = index + to_try.length
    tried.push(to_try)
    if new_index < path.length
      stack.push([new_index, []])
    end
  end

  main_funcs
end

def char_cost(path)
  comp_len = path
    .split(/(R|L)/)
    .filter{ |s| !s.empty? }
    .length
  comp_len + comp_len - 1
end

def find_substrings_of_length(string, length)
  substrings = {}
  (0..(string.length - length)).each do |i|
    sub = string[i, length]
    sub_range = Set[*(i..(i+length-1))]
    if substrings[sub]
      substrings[sub] += sub_range
    else
      substrings[sub] = sub_range
    end
  end
  substrings
end

def get_changes(orientation, coord)
  deltas = ORIENTATIONS[orientation].entries.map do |change, direction|
    [change, CARDINALS[direction]]
  end

  changes = {}
  deltas.each do |d|
    change_key, delta = d
    changes[change_key] = apply_delta(coord, delta)
  end
  changes
end

def apply_delta(coord, delta)
  [coord[0] + delta[0], coord[1] + delta[1]]
end

def get_starting_coord(coord_map)
  orientation = :up
  starting_coord, = coord_map
                    .entries
                    .detect { |_c, t| t == '^' }
  starting_coord
end

def get_adjacent_coords(coord)
  cardinals = {}
  CARDINALS.entries.each do |_c, d|
    cardinals[k] = [coord[0] + d[0], coord[1] + d[1]]
  end
end

def build_coord_map(output)
  x = 0
  y = 0
  coord_map = {}
  output.each do |o|
    if o == 10
      x = 0
      y += 1
    else
      coord_map[[x, y]] = o.chr
      x += 1
    end
  end
  coord_map
end

def paint_scaffold(output)
  text = ''
  output.each do |o|
    text += o.chr
  end
  text
end

def load_input(path = './input')
  f = File.open(path)
  text = f.read
  f.close
  text.split(',').map(&:to_i)
end

main if $PROGRAM_NAME == __FILE__