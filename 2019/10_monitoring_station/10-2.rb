require_relative('./10-1')
=begin

comparison function

takes coords a, b
compares quadrants
convert to absolute, compare slope ratio

=end

station = [26, 36]

def order_in_sequence_destroyed(outpost, asteroids)
    asteroids_without_outpost = asteroids.select {|a| a != outpost}
    centered_coords = center_coords_around_point(outpost, asteroids_without_outpost)
    slope_groups = get_slope_groups(centered_coords)
    slopes = sort_slopes(slope_groups.keys).select do |s|
        slope_groups[s] != nil
    end

    ordered_coords = []
    # puts "double: #{(slope_groups.values.select {|g| g.length == 2 }).count}"
    while slopes.length > 0
        slopes
            .each do |slope| 
                ordered_coords.push(slope_groups[slope].shift)
            end

        slopes = slopes.select { |s| slope_groups[s].any? }
    end

    ordered_coords.map do |c|
        c.zip(outpost)
            .map {|p| p.sum}
    end
end


def sort_slopes(slopes)
    # quadrants
    quadrants = [
        # q1
        slopes.select {|s| s[0] > 0 and s[1] > 0},
        # q2
        slopes.select {|s| s[0] < 0 and s[1] > 0},
        # q3
        slopes.select {|s| s[0] < 0 and s[1] < 0},
        # q4
        slopes.select {|s| s[0] > 0 and s[1] < 0},
    ]

    quadrants.map.with_index do |q, i|
        sort_quadrant_slopes_ascending(q, i % 2 != 0)
    end

    q1, q2, q3, q4 = quadrants

    [
        [1, 0],
        *q1,
        [0, 1],
        *q2,
        [-1, 0],
        *q3,
        [0, -1],
        *q4
    ]
end

def flip_coords(coords)
    coords.map { |c| c.reverse }
end


def sort_quadrant_slopes_ascending(slopes, is_q2_or_q4)
    sorted = slopes.sort_by do |coord| 
        x, y = coord
        -(coord[0].abs.to_f / coord[1].abs.to_f)
    end

    # if we're sorting q2 or q4, we have to flip the order
    sorted.reverse ? is_q2_or_q4 : sorted
end


# fails if you give 0, 0
def get_slope_groups(coords)
    slope_groups = {}
    coords.each do |coord|
        i, j = coord
        if i == 0
            slope = [0, j / (j.abs)]
        elsif j == 0
            slope = [i / (i.abs), 0]
        else
            gcd_for_coord = gcd(i.abs, j.abs)
            slope = [i / gcd_for_coord, j / gcd_for_coord]
        end

        point_slope = []

        if slope_groups.key? slope
            slope_groups[slope].push(coord)
        else
            slope_groups[slope] = [coord]
        end
    end

    slope_groups.keys.each do |slope|
        slope_groups[slope].sort! do |a, b| 
            abs_sum(a) <=> abs_sum(b)
        end
    end

    slope_groups
end

def abs_sum(arr)
    arr.map {|n| n.abs }
       .sum
end


def paint_sequence(asteroid_seq, input_path)
    alphabet = ("a".."z").to_a
    if asteroid_seq.length > alphabet.length
        raise "sequence too long! should be at most 26"
    end

    text = load_input(input_path)
    # puts "lines:  #{lines}"
    # puts "len: #{lines.length}"
    asteroid_seq.each_with_index do |coord, index|
        text = paint_coord(coord, alphabet[index], text)
    end

    text
end

def paint_slope_groups(groups, text)
    alphabet = ("a".."z").to_a
    text = text.dup

    slopes = groups.keys

    puts "len: #{slopes.length}"

    alphabet.each_with_index do |char, index|
        slope = slopes[index]
        puts "#{alphabet[index]}: #{slope.join(",")}"
        group = groups[slope]
        group.each do |coord|
            text = paint_coord(coord, char, text)
        end
    end
    puts text
end

def paint_coord(coord, char, text)
    lines = text.split("\n")
    puts "coord: #{coord}"
    puts "lines: #{lines.length}"
    i, j = coord
    line = lines[i]
    line[j]

    lines.join('\n')
end


def get_dimensions_and_asteroids(input_path="./input")
    parse_input(load_input(input_path))
end


def uncenter_coords(point, coords)
    i_origin, j_origin = point
    coords.map do |coord|
        i, j = coord

        [i + i_origin, j + j_origin]
    end
end


def paint_slopes
    input_path = "./test_inputs/4"
    dims, asteroids = get_dimensions_and_asteroids(input_path)
    outpost = [10, 12]
    centered_asteroids = center_coords_around_point(outpost, asteroids)
    centered_groups = get_slope_groups(centered_asteroids)
    groups = {}

    centered_groups.entries.each do |slope, group|
        puts "slope: #{slope}"
        puts "group: #{group}"
        groups[slope] = uncenter_coords(outpost, group)
        puts "uncentered: #{groups[slope]}"

        out_of_bounds = groups[slope].select do |coord|
            i, j = coord
            i_len, j_len = dims
            i >= i_len or j >= j_len or i < 0 or j < 0
        end

        if out_of_bounds.any?
            raise "group #{slope.join(",")} has an out of bounds coord"
        end
    end

    puts "dims: #{dims}"

    text = load_input(input_path)
    paint_slope_groups(groups, text)
end

if __FILE__ == $0
    paint_slopes
end