import functools
import itertools
import math
import re

from dataclasses import dataclass
from typing import Union

from typing_extensions import Self


@dataclass
class RegNum:
    value: int
    prev: Self = None
    next: Self = None

    def try_split(self, depth: int):
        if self.value < 10:
            return False

        left_value = math.floor(self.value / 2)
        right_value = math.ceil(self.value / 2)

        left = RegNum(left_value)
        right = RegNum(right_value)

        left.add_next(right)
        self.replace(left)
        return Pair(depth + 1, left, right)

    def replace(self, repl: Self, n: int = 1):
        if self.prev:
            self.prev.next = repl
            repl.prev = self.prev

        _next = self
        for i in range(n):
            _next = _next.next
        repl_tail = repl.tail()
        repl_tail.next = _next
        if _next:
            _next.prev = repl_tail

    def add_next(self, to_add):
        if to_add:
            to_add.prev = self
        self.next = to_add

    def add_prev(self, to_add):
        if to_add:
            to_add.next = self
        self.prev = to_add

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

    def __str__(self):
        return str(self.value)


@dataclass
class Pair:
    depth: int
    left: Union[RegNum, Self] = None
    right: Union[RegNum, Self] = None

    def magnitude(self):
        if type(self.left) == RegNum:
            leftval = self.left.value
        else:
            leftval = self.left.magnitude()
        if type(self.right) == RegNum:
            rightval = self.right.value
        else:
            rightval = self.right.magnitude()
        return leftval * 3 + rightval * 2

    def add(self, to_add: Self):
        self.reduce()
        to_add.reduce()

        right_regnum_self = self.rightmost().right
        left_regnum_to_add = to_add.leftmost().left
        right_regnum_self.add_next(left_regnum_to_add)

        combined = Pair(self.depth, left=self, right=to_add)
        for elt in (*self.traverse(), *to_add.traverse()):
            elt.depth += 1
        return combined.reduce()

    def reduce(self):
        was_transformed = True
        # print('original')
        while was_transformed:
            # print(self)
            # print()
            was_transformed, _ = self.try_explode()
            if was_transformed:
                # print('after explode')
                continue
            was_transformed = self.try_split()
            # print('after split')
        return self

    def try_explode(self):
        if self.is_reg_pair() and self.depth == 5:
            repl = RegNum(0)
            if self.left.prev:
                self.left.prev.value += self.left.value
            if self.right.next:
                self.right.next.value += self.right.value
            self.left.replace(repl, 2)
            return True, repl

        if type(self.left) == Pair:
            is_exploded, left_explode_num = self.left.try_explode()
            if left_explode_num:
                self.left = left_explode_num
            if is_exploded:
                return is_exploded, None

        if type(self.right) == Pair:
            is_exploded, right_explode_num = self.right.try_explode()
            if right_explode_num:
                self.right = right_explode_num
            if is_exploded:
                return is_exploded, None

        return False, None

    def leftmost(self):
        curr = self
        while type(curr.left) == Pair:
            curr = curr.left
        return curr

    def rightmost(self):
        curr = self
        while type(curr.right) == Pair:
            curr = curr.right
        return curr

    def try_split(self):
        if type(self.left) == RegNum:
            split_result = self.left.try_split(self.depth)
            if split_result:
                self.left = split_result
                return True
        elif self.left.try_split():
            return True

        if type(self.right) == RegNum:
            split_result = self.right.try_split(self.depth)
            if split_result:
                self.right = split_result
                return True
        elif self.right.try_split():
            return True

        return False

    def is_reg_pair(self):
        return type(self.left) == RegNum and type(self.right) == RegNum

    def traverse(self):
        if type(self.left) == Pair:
            for elt in self.left.traverse():
                yield elt
        if type(self.right) == Pair:
            for elt in self.right.traverse():
                yield elt
        yield self

    def __str__(self):
        ldisp = str(self.left)
        rdisp = str(self.right)
        return f'[{ldisp},{rdisp}]'


def example_add():
    examples = '''
      [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    + [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    = [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

      [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    + [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    = [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

      [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    + [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    = [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

      [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
    + [7,[5,[[3,8],[1,4]]]]
    = [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

      [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
    + [[2,[2,2]],[8,[8,1]]]
    = [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

      [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
    + [2,9]
    = [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

      [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
    + [1,[[[9,3],9],[[9,0],[0,7]]]]
    = [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

      [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
    + [[[5,[7,4]],7],1]
    = [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

      [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
    + [[[[4,2],2],6],[8,7]]
    = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
        
    '''
    examples = examples.strip()
    for ex in examples.split('\n\n'):
        orig, to_add, res = [l[l.index('['):].strip() for l in ex.split('\n')]
        orig = parse(orig)
        to_add = parse(to_add)

        added = orig.add(to_add)
        if str(added) != res:
            print('wtf')


def example():
    examples = [
        "[[1,2],[[3,4],5]]",  # becomes 143.
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",  # becomes 1384.
        "[[[[1,1],[2,2]],[3,3]],[4,4]]",  # becomes 445.
        "[[[[3,0],[5,3]],[4,4]],[5,5]]",  # becomes 791.
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",  # becomes 1137.
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",  # becomes 3488.
    ]
    for ex in examples:
        parsed = parse(ex)
        print(parsed, '= ', str(parsed.magnitude()))


def parse_input():
    with open('./input') as f:
        text = f.read().strip()
    to_sum = [parse(line.strip()) for line in text.split('\n')]
    return to_sum


def p1():
    s_nums = parse_input()
    summed = s_nums[0]
    for i, elt in enumerate(s_nums[1:], start=1):
        summed = summed.add(elt)
    print(summed)
    print(summed.magnitude())
    print()


def p2():
    with open('./input') as f:
        s_nums_raw = [l.strip() for l in f.read().strip().split()]
    max_mag = 0
    for sn1, sn2 in itertools.combinations(s_nums_raw, 2):
        for sn1, sn2 in itertools.permutations([sn1, sn2]):
            elt1, elt2 = parse(sn1), parse(sn2)
            added = elt1.add(elt2)
            mag = added.magnitude()
            if max_mag < mag:
                max_mag = mag
    print(max_mag)


def parse(text_raw):
    idx = 0
    depth = 0
    stack = []
    is_left = True
    regnum_tail = None
    while idx < len(text_raw):
        if text_raw[idx] == '[':
            depth += 1
            stack.append(Pair(depth))
            if len(stack) > 1:
                if is_left:
                    stack[-2].left = stack[-1]
                else:
                    stack[-2].right = stack[-1]
            is_left = True
            idx += 1
            continue
        if text_raw[idx] == ']':
            depth -= 1
            idx += 1
            # last iteration will return root elt here
            root_elt = stack.pop()
            continue
        if text_raw[idx] == ',':
            is_left = False
            idx += 1
            continue

        match = re.match('^(\d+)', text_raw[idx:])
        if not match:
            raise Exception(f"unable to match: {text_raw[idx:]}")
        value = int(match.groups()[0])
        regnum = RegNum(value)
        regnum.add_prev(regnum_tail)
        regnum_tail = regnum

        if is_left:
            (stack[-1]).left = regnum
        else:
            (stack[-1]).right = regnum
        idx += len(str(value))
    return root_elt


if __name__ == '__main__':
    p1()
    p2()
