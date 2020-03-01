#!/usr/bin/env ruby

=begin
<x=-15, y=1, z=4>
<x=1, y=-10, z=-8>
<x=-5, y=4, z=9>
<x=4, y=6, z=-2>
=end

def main
    simulate(1000)
end

def simulate(cycles) 
    moons = {
        a: {pos: {x:-15, y:  1, z: 4}, vel: {x: 0, y: 0, z: 0}},
        b: {pos: {x:  1, y:-10, z:-8}, vel: {x: 0, y: 0, z: 0}},
        c: {pos: {x: -5, y:  4, z: 9}, vel: {x: 0, y: 0, z: 0}},
        d: {pos: {x:  4, y:  6, z:-2}, vel: {x: 0, y: 0, z: 0}},
    }

    cycles.times.each do |step|
        apply_gravity(moons)
        apply_velocity(moons)
        puts "#{total_energy(moons)} (#{step + 1})"
    end
end

def total_energy(moons)
    moon_totals = moons.values.map do |moon|
        potential_energy(moon) * kinetic_energy(moon)
    end

    moon_totals.sum
end

def potential_energy(moon)
    dims = moon[:pos].values
    dims.map {|v| v.abs}
        .sum
end

def kinetic_energy(moon)
    dims = moon[:vel].values
    dims.map {|v| v.abs}
        .sum
end

def apply_gravity(moons)
    vel_deltas = {}
    moons.keys.each {|k| vel_deltas[k] = {x: 0, y: 0, z: 0}}

    pairs = moons.entries.combination(2).to_a

    # calculate deltas
    pairs.each do |pair|
        a,b = pair
        a_key, a_val = a
        b_key, b_val = b
        [:x,:y,:z].each do |dim|
            case a_val[:pos][dim] <=> b_val[:pos][dim]
            when 1
                vel_deltas[a_key][dim] -= 1
                vel_deltas[b_key][dim] += 1
            when -1
                vel_deltas[a_key][dim] += 1
                vel_deltas[b_key][dim] -= 1
            end
        end
    end

    # apply deltas
    moons.keys.each do |k|
        [:x,:y,:z].each do |dim|
            moons[k][:vel][dim] += vel_deltas[k][dim]
        end
    end
end

def apply_velocity(moons)
    moons.values.each do |moon|
        [:x, :y, :z].each do |dim|
            moon[:pos][dim] += moon[:vel][dim]
        end
    end

    moons
end


if __FILE__ == $0
    main
end