from enum import Enum
from typing import NamedTuple, Dict, List


class PacketType(Enum):
    LITERAL = 4


class Segment(NamedTuple):
    len: int
    type: any


class Header(NamedTuple):
    version: int
    type_id: int


class LiteralPacket(NamedTuple):
    header: Header
    number: int


class OperatorPacket(NamedTuple):
    header: Header
    length_type: bin
    length: int
    sub_packets: List[any]


str_rep = None
pointer = 0

with open('./input') as f:
    text = f.read().strip()

examples = [
    text,
    # '8A004A801A8002F478',
    # '620080001611562C8802118E34',
    # 'C0015000016115A2E0802F182340',
    # 'A0016C880162017C3686B18A3D4780',
]


def main():
    global str_rep, pointer
    for example in examples:
        pointer = 0
        str_rep = bin(int(example, 16))[2:].zfill(len(example) * 4)

        oft_disp = ''
        hex_disp = ''
        bin_disp = ''
        for i in range(0, len(example)):
            oft_disp += str(i).ljust(4, ' ') + ' '
            hex_disp += example[i].ljust(4, ' ') + ' '
            bin_disp += str_rep[i * 4: i * 4 + 4] + ' '
        print(oft_disp)
        print(hex_disp)
        print(bin_disp)

        root_packet = parse_packet()
        print(root_packet)
        packets = [p for p in yield_all_packets(root_packet)]
        sum_versions = sum(p.header.version for p in packets)
        print(sum_versions)
        print()


def yield_all_packets(packet):
    yield packet
    if packet.header.type_id == PacketType.LITERAL.value:
        pass
    else:
        for sub_packet in packet.sub_packets:
            for elt in yield_all_packets(sub_packet):
                yield elt


def bin_as_int(b):
    return int(b, 2)


def as_bin(b):
    return bin(bin_as_int(b))


def as_str(b):
    return b


def parse_packet():
    packet_start = pointer
    version = parse_segment(Segment(3, bin_as_int))
    type_id = parse_segment(Segment(3, bin_as_int))
    header = Header(version, type_id)
    if header.type_id == PacketType.LITERAL.value:
        packet_start_pointer = pointer
        sub_bits = ''
        cont = parse_segment(Segment(1, as_bin))
        sub_bits += parse_segment(Segment(4, as_str))
        while cont == '0b1':
            cont = parse_segment(Segment(1, as_bin))
            sub_bits += parse_segment(Segment(4, as_str))
        # pass_leftovers(packet_start_pointer)
        number = bin_as_int(sub_bits)
        return LiteralPacket(header, number)

    length_type_id = parse_segment(Segment(1, as_bin))

    sub_packets = []
    if length_type_id == '0b0':
        sub_packet_length = parse_segment(Segment(15, bin_as_int))
        pointer_at_start = pointer
        while pointer < (pointer_at_start + sub_packet_length):
            sub_packets.append(parse_packet())
    else:
        sub_packet_length = parse_segment(Segment(11, bin_as_int))
        for p_idx in range(sub_packet_length):
            sub_packets.append(parse_packet())
    return OperatorPacket(header, length_type_id, sub_packet_length, sub_packets)


def pass_leftovers(starting_pointer):
    global pointer
    hex_leftovers = (4 - ((pointer - starting_pointer) % 4)) % 4
    pointer += hex_leftovers
    print(pointer)


def parse_segment(segment):
    global pointer
    str_segment = str_rep[pointer:segment.len + pointer]
    value = segment.type(str_segment)
    pointer += segment.len
    return value


def test():
    inputA = int('0101', 2)
    print("Before shifting " + str(inputA) + " " + bin(inputA))
    print("After shifting in binary: " + bin(inputA << 1))
    print("After shifting in decimal: " + str(inputA << 1))


conv_table = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def parse_input(path='./input'):
    return example3_operator
    with open(path) as f:
        text = f.read()
    return str(bin(int(example1, 16)))[2:]


if __name__ == '__main__':
    main()
