def load_input(path="./input")
    file = open(path, 'r')
    text = file.read
    file.close

    text.split('').map { |c| c.to_i }
end


def solve1(width, height)
    all_cells = load_input
    picture_length = width * height

    square_coords = (0..(all_cells.length - 1)).step(picture_length).to_a

    lowest_zero_count = Float::INFINITY
    most_zeros = nil
    puts "leftover: #{all_cells.length % picture_length}"

    for i in square_coords
        cells = all_cells.slice(i, picture_length)
        puts "cells: #{cells}"
        zero_count = cells.count(0)
        if lowest_zero_count > zero_count
            most_zeros = cells
            lowest_zero_count = zero_count
        end
    end

    most_zeros.count(1) * most_zeros.count(2)
end


if __FILE__ == $0
    puts solve1(25, 6)
end