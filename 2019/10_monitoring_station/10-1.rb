require 'set'

def find_best_outpost(input_path="./input")
    input = load_input(input_path)
    dimensions, asteroid_coords = parse_input(input)

    highest_asteroid_count = 0
    best_outpost_location = asteroid_coords.first

    asteroid_coords.each do |potential_outpost|
        centered_asteroids = center_coords_around_point(potential_outpost, asteroid_coords) 

        visible_asteroids = Set[]
        centered_asteroids.each do |asteroid|
            i, j = asteroid
            if i == 0 && j == 0
            elsif i == 0
                visible_asteroids.add([0, j / (j.abs)])
            elsif j == 0
                visible_asteroids.add([i / (i.abs), 0])
            else
                common_divisor = gcd(i.abs, j.abs)
                visible_asteroids.add([i / common_divisor, j / common_divisor])
            end
        end

        if potential_outpost == [5,8]
            puts visible_asteroids.length
        end

        if visible_asteroids.length > highest_asteroid_count
            highest_asteroid_count = visible_asteroids.length
            best_outpost_location = potential_outpost
        end
    end

    return [*(best_outpost_location.reverse), highest_asteroid_count]
end


def center_coords_around_point(point, coords)
    i_origin, j_origin = point
    coords.map do |coord|
        i, j = coord 
        [i - i_origin, j - j_origin]
    end
end

def parse_input text
    lines = text.split
    dimensions = [lines.length, lines[0].length]

    asteroid_coords = Set[]
    lines.each_with_index do |line, i|
        line.split('').each_with_index do |char, j|
            if char == '#'
                asteroid_coords.add([i, j])
            end
        end
    end

    return [dimensions, asteroid_coords]
end

def load_input(path="./input")
    f = open(path, 'r')
    text = f.read()
    f.close
    return text
end

def get_all_coords(dimensions)
    height, width = dimensions
    coords = Set[]
    (0..height).each do |i|
        (0..width).each do |j|
            coords.add([i,j])
        end
    end

    return coords
end

def gcd (a, b)
    while b != 0
        b, a = a % b, b
    end
    return a
end

if __FILE__ == $0
    puts find_best_outpost
end