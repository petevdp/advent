require_relative '../intcode'

RSpec.describe IntCode, '#run' do

    it "can sum numbers" do
        summing_program = [1,2,2, 0, 99] # add 2 + 2, store at position 0 and exit
        sum = 4
        computer = IntCode.new(summing_program, [])
        computer.run()

        expect(computer.register[0]).to eq(sum)
    end

    it "halts on opcode 99", :focus do
        program = [99]

        computer = IntCode.new(program, [])
        computer.run()

        expect(computer.curr_position).to eq(nil)
    end

    it "can multiply numbers" do
        summing_program = [1,2,5, 0, 99] # add 2 + 2, store at position 0 and exit
        product = 10
        computer = IntCode.new(summing_program, [])
        computer.run()

        expect(computer.register[0]).to eq(product)
    end
end