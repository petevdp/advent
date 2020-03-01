#!/usr/bin/env ruby

require_relative("./11-1")

def main
    tile_colors = get_tile_colors({[0,0] => 1})
    puts print_tiles(tile_colors)
end

def print_tiles tile_colors
    x_min, y_min, x_max, y_max = get_tile_dimensions(tile_colors)

    tile_arr = (y_min..y_max).map do |i|
        (x_min..x_max).map do |j|
            tile_colors[[i,j]] == 1 ? "#" : "."
        end
    end

    tile_arr
        .map {|row| row.reverse.join}
        .reverse
        .join("\n")
end

def get_tile_dimensions(tile_colors)
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0

    tile_colors.keys.each do |coord|
        y, x = coord

        x_min = [x, x_min].min
        y_min = [y, y_min].min
        x_max = [x, x_max].max
        y_max = [y, y_max].max
    end

    [x_min, y_min, x_max, y_max]
end


if __FILE__ == $0
    main
end