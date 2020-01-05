require "erb"

$WIDTH = 25
$HEIGHT = 6
$PICTURE_LENGTH = $WIDTH * $HEIGHT

def load_input(path="./input")
    file = open(path, 'r')
    text = file.read
    file.close

    text.split('').map { |c| c.to_i }
end

def get_layers all_pixels
    layer_coords = (0..all_pixels.length - 1).step($PICTURE_LENGTH).to_a

    layer_coords.map do |i|
        all_pixels.slice(i, $PICTURE_LENGTH)
    end
end

def squash_pixel_layers pixel_layers
    shown, *rest = pixel_layers

    rest.each do |layer|
        if shown == 2 # 2 is transparent
            shown = layer
        end
    end

    shown
end

def solve name
    all_pixels = load_input
    first, *rest = get_layers all_pixels

    pixels = first
        .zip(*rest)
        .map { |p_l| squash_pixel_layers p_l }

    File.write(name+".html", Picture.new(pixels).render)
end

class Picture
    attr_reader :rows
    def initialize(pixels, template_path="template.erb")

        @template = File.open(template_path, 'rb', &:read)
        @pixels = pixels
    end

    def render
        ERB.new(@template).result(binding)
    end
end

if __FILE__ == $0
    solve ARGV[0]
end