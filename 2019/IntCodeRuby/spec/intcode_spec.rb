require_relative '../intcode'

RSpec.describe IntCode, '#run' do
    it "it can sum numbers" do
        summing_program = [1,2,2, 0, 99] # add 2 + 2, store at position 0 and exit
        sum = 4
        computer = IntCode.new(summing_program, [])
        computer.run()

        expect(computer.register[0]).to eq(sum)
    end
    it "it can multiply numbers" do
        summing_program = [1,2,5, 0, 99] # add 2 + 2, store at position 0 and exit
        product = 10
        computer = IntCode.new(summing_program, [])
        computer.run()

        expect(computer.register[0]).to eq(product)
    end
end