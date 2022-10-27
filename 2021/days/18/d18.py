import functools
import math
import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple, List
from typing_extensions import Self


@dataclass
class SNReg:
    value: int
    depth: int
    is_left: bool
    next: Self = None
    prev: Self = None

    def unlink_prev(self):
        if not self.prev:
            return

        if not self.prev.prev:
            self.prev = None
            return

        self.prev.prev.next = self
        self.prev = self.prev.prev

    def unlink_next(self):
        if not self.next:
            return

        if not self.next.next:
            self.next = None
            return

        self.next.next.prev = self
        self.next = self.next.next

    def replace(self, elt: Self):
        if self.prev:
            self.prev.next = elt
            elt.prev = self.prev
        if not self.next:
            return
        elt_tail = elt.tail()
        elt_tail.next = self.next
        self.next.prev = elt_tail

    def tail(self):
        curr = self
        while curr.next:
            curr = curr.next
        return curr

    def head(self):
        curr = self
        while curr.prev:
            curr = curr.prev
        return curr

    def elts(self):
        curr = self.head()
        while curr:
            yield curr
            curr = curr.next

    def is_parent_left(self):
        if not self.is_left: raise Exception("is_parent_left only works on left elts")
        return (not self.prev) or (not self.prev.is_left)


def example():
    example_left = "[[1,2],[[3,4],5]]"
    example_right = "[[3,4],5]"
    print(example_left)
    print(example_right)
    example_left = parse(example_left)
    example_right = parse(example_right)

    # added = add(example_left, example_right)
    print_sn(example_left)
    print()
    mag = magnitude(example_left)
    print(f'{mag=}')


def main():
    with open('./input') as f:
        lines = f.read().strip().split('\n')

    snums = [parse(l) for l in lines]
    res = functools.reduce(add, snums)
    print()
    print()
    print_sn(res)
    print(magnitude(res))


def magnitude(sn):
    sn = deepcopy(sn)

    while pair := find_regular_pair(sn):
        left, right = pair
        added_value = left.value * 3 + right.value * 2
        # repl = SNReg(added_value, depth=left.depth - 1, is_left=left.is_parent_left())
        left.value = added_value
        left.depth -= 1
        left.is_left = left.is_parent_left()
        left.unlink_next()
        sn = left.head()
        print_sn(sn)
        print()
    # if there are no regular pairs left, there is only one element left in the linked list, which is the last value
    return sn.value


def reduce(snum: SNReg):
    explodes_left = True
    splits_left = True
    iter = 0
    print("initial")
    print_sn(snum)
    print()
    while splits_left or explodes_left:
        snum, explodes_left = explode(snum)
        print(iter)
        if explodes_left:
            print("after explode")
            print_sn(snum)
            print()
            iter += 1
            continue
        snum, splits_left = split(snum)
        print("after plit")
        print_sn(snum)
        print()
        iter += 1
    return snum


def add(left: SNReg, right: SNReg):
    tail_left = left.tail()
    head_right = right.head()
    tail_left.next = head_right
    head_right.prev = tail_left

    for elt in left.elts():
        elt.depth += 1
    return reduce(left.head())


def print_sn(sn_head: SNReg):
    for elt in sn_head.elts():
        print(f"{'-' * elt.depth} : {str(elt.value).ljust(3, ' ')} : {'left' if elt.is_left else 'right'}")


def explode(start: SNReg):
    pair = find_regular_pair(start, 4)
    if not pair:
        return start, False
    elt1, elt2 = pair

    replacement = SNReg(value=0, depth=elt1.depth - 1, is_left=elt1.is_parent_left())

    if elt1.prev:
        elt1.prev.value += elt1.value

    if elt2.next:
        elt2.next.value += elt2.value

    elt1.unlink_next()
    elt1.replace(replacement)

    return replacement.head(), True


def split(start: SNReg):
    curr = start
    while curr:
        if curr.value < 10:
            curr = curr.next
            continue
        replacement_left = SNReg(value=math.floor(curr.value / 2), depth=curr.depth + 1, is_left=True)
        replacement_right = SNReg(value=math.ceil(curr.value / 2), depth=curr.depth + 1, is_left=False)
        replacement_left.next = replacement_right
        replacement_right.prev = replacement_left
        replacement_left.next_is_paired = True
        curr.replace(replacement_left)
        return replacement_left.head(), True
    return start, False


def find_regular_pair(sn, depth=None):
    for elt in sn.elts():
        if elt.is_left and elt.next and elt.depth == elt.next.depth and depth is None or elt.depth == depth:
            return elt, elt.next
    return False


def parse(text_raw):
    idx = 0
    curr_tail = None
    head = None
    depth = 0
    is_left_num = True
    while idx < len(text_raw):
        if text_raw[idx] == '[':
            depth += 1
            is_left_num = True
            idx += 1
            continue
        if text_raw[idx] == ']':
            depth -= 1
            idx += 1
            is_left_num = False
            continue
        if text_raw[idx] == ',':
            is_left_num = False
            idx += 1
            continue

        match = re.match('^(\d+)', text_raw[idx:])
        if not match:
            raise Exception(f"unable to match: {text_raw[idx:]}")
        value = int(match.groups()[0])
        sn = SNReg(value, depth, is_left_num)
        if not curr_tail:
            head = sn
        else:
            curr_tail.next = sn
            sn.prev = curr_tail
        curr_tail = sn
        idx += len(str(value))
    return head


if __name__ == '__main__':
    example()
