import math
from enum import Enum
from typing import NamedTuple, Dict, List


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


class Segment(NamedTuple):
    len: int
    type: any


class Header(NamedTuple):
    version: int
    type_id: int


class LiteralPacket(NamedTuple):
    header: Header
    value: int


class OperatorPacket(NamedTuple):
    header: Header
    length_type: bin
    length: int
    sub_packets: List[any]
    value: int


str_rep = None
pointer = 0

examples = [
    'C200B40A82',
    '04005AC33890',
    '880086C3E88112',
    'CE00C43D881120',
    'D8005AC2A8F0',
    'F600BC2D8F',
    '9C005AC2F8F0',
    '9C0141080250320F1802104A08',
]


def main():
    global str_rep, pointer
    data = parse_input()

    pointer = 0
    str_rep = data

    oft_disp = ''
    hex_disp = ''
    bin_disp = ''
    for i in range(0, len(data)):
        oft_disp += str(i).ljust(4, ' ') + ' '
        hex_disp += data[i].ljust(4, ' ') + ' '
        bin_disp += str_rep[i * 4: i * 4 + 4] + ' '
    print(oft_disp)
    print(hex_disp)
    print(bin_disp)

    root_packet = parse_packet()
    print(f'value: {root_packet.value}')
    print()


def run_examples():
    global str_rep, pointer
    for example in examples:
        print(example)
        pointer = 0
        str_rep = parse_hex(example)
        root_packet = parse_packet()
        print(root_packet.value)
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

    sub_vals = [sp.value for sp in sub_packets]
    match header.type_id:
        case PacketType.SUM.value:
            value = sum(sub_vals)
        case PacketType.PRODUCT.value:
            value = math.prod(sub_vals)
        case PacketType.MINIMUM.value:
            value = min(sub_vals)
        case PacketType.MAXIMUM.value:
            value = max(sub_vals)
        case PacketType.GREATER_THAN.value:
            val1 = sub_packets[0].value
            val2 = sub_packets[1].value
            value = int(val1 > val2)
        case PacketType.LESS_THAN.value:
            val1 = sub_packets[0].value
            val2 = sub_packets[1].value
            value = int(val1 < val2)
        case PacketType.EQUAL_TO.value:
            val1 = sub_packets[0].value
            val2 = sub_packets[1].value
            value = int(val1 == val2)
        case _:
            raise Exception(f"unhandled packet type {header.type_id}")

    return OperatorPacket(header, length_type_id, sub_packet_length, sub_packets, value)


def parse_segment(segment):
    global pointer
    str_segment = str_rep[pointer:segment.len + pointer]
    value = segment.type(str_segment)
    pointer += segment.len
    return value


def parse_hex(text):
    return bin(int(text, 16))[2:].zfill(len(text) * 4)


def parse_input(path='./input'):
    with open(path) as f:
        text = f.read().strip()

    return parse_hex(text)


if __name__ == '__main__':
    main()
