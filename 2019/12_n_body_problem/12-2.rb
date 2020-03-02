#!/usr/bin/env ruby

require "set"
require "json"
require_relative "./12-1"

test_ans = 4686774924

def main
    moons = load_input()
    first, *rest = find_cycles_for_dims(moons)
    puts [first, *rest].to_s
    puts rest.reduce(first, :lcm)
end

def find_cycles_for_dims(moons, max_ticks=Float::INFINITY)
    dims = Set[*moons.values[0][:pos].keys]
    tick = 0
    previous = create_dims_arrs(dims)
    cycles = []

    while true
        run_tick(moons, dims)

        moons_by_dims = sort_by_dims(moons, dims)
        dims.each do |d|
            cycle_tick = previous[d].index(moons_by_dims[d])

            if cycle_tick
                puts "cycle: #{tick}, #{cycle_tick}, #{tick - cycle_tick} #{moons_by_dims[d]}"
                cycles.push(tick - cycle_tick)
                dims.delete(d)
            end
        end

        if tick == 0
            previous.keys.each do |d|
                previous[d].push(moons_by_dims[d])
            end
        end

        if cycles.length == 3
            return cycles
        end

        tick += 1
    end
end

def sort_by_dims(moons, dims)
    by_dims = {}
    dims.each do |d|
        moon_vals = {}
        moons.entries.each do |k, m|
            moon_vals[k] = {pos: m[:pos][d], vel: m[:vel][d]}
        end
        by_dims[d] = moon_vals
    end

    by_dims
end


def create_dims_arrs(dims)
    dims_sets = {}
    dims.each do |d|
        dims_sets[d] = []
    end

    dims_sets
end


def run_tick(moons, dims)
    apply_gravity(moons, dims.to_a)
    apply_velocity(moons, dims.to_a)
end

def clone hash
    JSON.parse(JSON.generate(hash), {symbolize_names: true})
end

def load_input(path="./input")
    f = open(path)
    lines = f.readlines
    f.close
    moons = lines.map do |l|
        moon = {}
        l = l.strip
        l = l[1..-2]
        words = l.split(",")

        words.each do |w|
            w = w.strip
            moon[w[0].to_sym] = w[2..-1].to_i
        end
        moon
    end
    alphabet = (:a..:z).to_a

    moon_hash = {}
    moons.zip(alphabet).each do |moon_pos, char|
        vel = {}
        moon_pos.keys.each { |k| vel[k] = 0 }
        moon_hash[char] = {pos: moon_pos, vel: vel}
    end
    moon_hash
end


if __FILE__ == $0
    main
end
