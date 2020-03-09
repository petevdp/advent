#!/usr/bin/env ruby
require "set"
require "gosu"
require "gosu/all"

require_relative "../IntCodeRuby/intcode"

MOVE_DELTAS = {
    1 => [0, -1], # north
    2 => [0, 1],  # south
    3 => [-1, 0], # west
    4 => [1, 0]   # east
}

DELTAS_MOVE = {
    [0, -1] => 1, # north
    [0, 1] => 2,  # south
    [-1, 0] => 3, # west
    [1, 0] => 4   # east

}

class Maze
    attr_reader :path, :visited, :walls
    def initialize
        @path = [[0,0]]
        @visited = {}
        @walls = Set[]
        @next_move = 1
        @min_distance = Float::INFINITY
        @max_distance = -Float::INFINITY
        @finding_o2 = true
        @computer = IntCode.new(
            load_input,
            [],
            -> { on_input },
            -> (output) { on_output(output) }
        )
    end

    def run
        @computer.run
    end

    private

    def on_input
        puts "curr: #{curr_coord}"
        adjacent = get_adjacent(curr_coord)
        candidates = adjacent
            .select {|c| !@path.include?(c) }
            .select { |c| (not @visited.include?(c)) or (@visited[c] > (@path.length + 1)) }
            .select do |c|
                not @walls.any? { |w| w.include?(curr_coord) and w.include?(c) }
            end

        coord = candidates[0]


        if @min_distance <= @path.length or coord == nil
            if @path.length <= 1
                puts "min distance: #{@min_distance}"
            end
            coord = prev_coord
        end

        @next_move = get_next_move_from_coord(coord)
        @next_move
    end

    def on_output(output)
        if next_coord == prev_coord
            @path.pop()
            puts "backtracking"
            return
        end

        case output
        when 0
            puts "wall hit: #{next_coord}"
            @walls.add(Set[curr_coord, next_coord])
        when 1
            puts "moved to: #{next_coord}"
            @visited[next_coord] = @path.length + 1
            @path.push(next_coord)
            @max_distance = [@max_distance, @path.length].max
        when 2
            if @finding_o2
                puts "2 found at #{next_coord}"
                @visited = {next_coord => 1}
                @path = [next_coord]
                @max_distance = 0
                @finding_o2 = false
            end
        end

        puts "len: #{@path.length}"
        puts "max: #{@max_distance - 1}"
    end

    def curr_coord
        @path[-1]
    end


    def next_coord
        x,y = curr_coord
        dx,dy = MOVE_DELTAS[@next_move]
        [x+dx, y+dy]
    end

    def prev_coord
        @path[-2]
    end

    def get_next_move_from_coord(coord)
        cx, cy = curr_coord
        nx, ny = coord
        delta = [(nx - cx), (ny - cy)]
        DELTAS_MOVE[delta]
    end

    def get_adjacent(coord)
        deltas = [
            [-1, 0],
            [1, 0],
            [0, -1],
            [0, 1]
        ]

        deltas.map { |d| [d[0] + coord[0], d[1] + coord[1]] }
    end
end

def load_input(path="./input")
    f = File.open(path)
    text = f.read()
    f.close

    text.split(",").map(&:to_i)
end

class DeadCell < Gosu::Grid::Cell
    def size
      object.width
    end
  
    private
  
    def object
      @object ||= Gosu::Image.new(window, 'assets/dead_cell.png', true)
    end
end



class PathCell < Gosu::Grid::Cell
    def size
      tiles.first.width
    end
  
    private
  
    def tiles
      @tiles ||= Gosu::Image.load_tiles(window, 'assets/live_cells.png', 18, 18, true)
    end
  
    def object
      tiles[0];
    end
end

class MazeGrid < Gosu::Window
    def initialize(maze)
        super(540, 320, false)
        @grid = Gosu::Grid.new(self)
        @maze = maze
        @grid.default_cell = DeadCell.new(self, 0, 0)
    end

    def update
        @grid.cells.clear
        @grid.cells.concat(@maze.path.map {|c| PathCell.new(self, *c)})
    end

    def draw
        @grid.draw
    end
end
  

if __FILE__ == $0
    maze = Maze.new
    maze.run
end