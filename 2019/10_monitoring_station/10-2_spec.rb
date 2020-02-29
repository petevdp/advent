require_relative "./10-2"



describe  "order_in_sequence_destroyed" do
    input_path = "./test_inputs/4"
    dimensions, asteroids = get_dimensions_and_asteroids(input_path)
    outpost = [13,11]

    ordered = order_in_sequence_destroyed(outpost, asteroids)

    it "first" do
        expect(ordered[0]).to eq([12,11])
    end
    it "2nd" do
        expect(ordered[1]).to eq([1,12])
    end
    it "3rd" do
        expect(ordered[2]).to eq([2,12])
    end
    it "10th" do
        expect(ordered[9]).to eq([8,12])
    end
    it "20th" do
        expect(ordered[19]).to eq([0,16])
    end
    # The 50th asteroid to be vaporized is at 16,9.
    it "50th" do
        expect(ordered[49]).to eq([9,16])
    end
    # The 100th asteroid to be vaporized is at 10,16.
    it "100th" do
        expect(ordered[99]).to eq([16,10])
    end

    # The 199th asteroid to be vaporized is at 9,6.
    it "199th" do
        expect(ordered[198]).to eq([6,9])
    end

    # The 200th asteroid to be vaporized is at 8,2.
    it "200th" do
        expect(ordered[199]).to eq([2,8])
    end

    # The 201st asteroid to be vaporized is at 10,9.
    it "201st" do
        expect(ordered[200]).to eq([9,10])
    end

    # The 299th and final asteroid to be vaporized is at 11,1.
    it "299th" do
        expect(ordered[-1]).to eq([1,11])
    end

    puts paint_sequence([outpost, *ordered], input_path)
end