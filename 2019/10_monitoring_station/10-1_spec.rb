require_relative './10-1'

TEST_DIR = "./test_inputs/"

describe "find_best_outpost" do

    it "passes example 1" do 
        expect(find_best_outpost(TEST_DIR + "1")).to eq([5,8,33])
    end
    it "passes example 2" do
        expect(find_best_outpost(TEST_DIR + "2")).to eq([1,2,35])
    end
    it "passes example 3" do
        expect(find_best_outpost(TEST_DIR + "3")).to eq([6,3,41])
    end
    it "passes example 4" do
        expect(find_best_outpost(TEST_DIR + "4")).to eq([11,3,210])
    end
end