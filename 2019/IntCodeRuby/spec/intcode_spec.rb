require_relative '../intcode'

RSpec.describe IntCode, '#run' do

    it "halts on opcode 99" do
        program = [99]

        computer = IntCode.new(program, [])
        computer.run()

        expect(computer.curr_position).to eq(nil)
    end

    it "can sum numbers" do
        summing_program = [1101,2,2, 0, 99] # add 2 + 2, store at position 0 and exit
        sum = 4
        computer = IntCode.new(summing_program, [])
        computer.run()

        expect(computer.register[0]).to eq(sum)
    end


    it "can multiply numbers" do
        multiplication_program = [1102, 2,5, 0, 99] # add 2 + 2, store at position 0 and exit
        product = 10
        computer = IntCode.new(multiplication_program, [])
        computer.run

        expect(computer.register[0]).to eq(product)
    end

    it "can receive input and emit output" do
        num = 40
        computer = IntCode.new([3,0,4,0,99], [num])
        computer.run

        expect(computer.outputs[0]).to eq(num)
    end

    describe "jump commands" do
        is_input_true_program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

        it "outputs 1 with true input" do
            computer = IntCode.new(is_input_true_program, [1])
            computer.run
            puts "outputs: #{computer.outputs}"
            expect(computer.outputs[0]).to eq(1)
        end

        it "outputs 0 with false input" do
            computer = IntCode.new(is_input_true_program, [0])
            computer.run
            expect(computer.outputs[0]).to eq(0)
        end
    end

    describe "equals" do
        # Using position mode, consider whether the input is
        # equal to 8; output 1 (if it is) or 0 (if it is not)
        program = [3,9,8,9,10,9,4,9,99,-1,8]

        it "outputs true when given 8" do
            computer = IntCode.new(program, [8])
            computer.run

            expect(computer.outputs[0]).to eq(1)
        end

        it "outputs false when not given 8" do
            computer = IntCode.new(program, [9])
            computer.run

            expect(computer.outputs[0]).to eq(0)
        end
    end

    describe "less than" do

        # Using immediate mode, consider whether the input is less than 8
        # output 1 (if it is) or 0 (if it is not)
        program = [3,3,1107,-1,8,3,4,3,99]

        it "outputs true when given input less than 8" do
            computer = IntCode.new(program, [7])
            computer.run

            expect(computer.outputs[0]).to eq(1)
        end

        it "outputs false when not given input not less than 8" do
            computer = IntCode.new(program, [8])
            computer.run

            expect(computer.outputs[0]).to eq(0)
        end
    end
end