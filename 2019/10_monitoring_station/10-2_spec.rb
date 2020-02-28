require_relative "./10-2"



describe  "order_in_sequence_destroyed" do
    input_path = "./test_inputs/4"
    dimensions, asteroids = get_dimensions_and_asteroids(input_path)
    outpost = [11, 13]

    ordered = order_in_sequence_destroyed(outpost, asteroids)

    it "first" do
        expect(ordered[0]).to eq([11,12])
    end
    it "2nd" do
        expect(ordered[1]).to eq([12,1])
    end
    it "3rd" do
        expect(ordered[2]).to eq([12,2])
    end
    it "10th" do
        expect(ordered[9]).to eq([12,8])
    end
    it "20th" do
        expect(ordered[19]).to eq([16,0])
    end
    it "100th" do
        expect(ordered[99]).to eq([10,16])
    end
    it "201st" do
        expect(ordered[200]).to eq([10,9])
    end
    it "299" do
        expect(ordered[298]).to eq([11,1])
    end
    puts paint_sequence([outpost, *ordered.first(25)], input_path)
end