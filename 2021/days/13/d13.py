from typing import NamedTuple
import re


class Point(NamedTuple):
    x: int
    y: int

class Fold(NamedTuple):
    axis: str
    value: in
    t


def get_input(path="./days/13/test"):
    with open(path) as f:
        points_raw, folds_raw = f.read().strip().split("\n\n")

    points = {Point(*(int(n) for n in l.split(','))) for l in points_raw.strip().split("\n")}
    folds = [parse_fold(l) for l in folds_raw.strip().split('\n')]
    return points,folds
    

def parse_fold(line):
    axis, value = re.match(r".*(\w)=(\d+).*", line).groups()
    return Fold(axis, int(value))



POINTS, FOLDS = get_input()



def set_point_axis(point, axis, value):
    if axis == 'x':
        return Point(value, point.y)
    else:
        return Point(point.x, value)
    
# def compare_points(a,b):
#     if a.y > b.y:
#         return 1
#     if a.y < b.y:
#         return -1
#     if a.x > b.x:
#         return 1
#     if a.x < b.x:
#         return -1
def max_point_for_axis(points, axis):
    return max(getattr(p, axis) for p in points) + 1
    

def print_points(points):
    arr = [[False for n in range(max_point_for_axis(points, 'x'))] for n in range(max_point_for_axis(points, 'y'))]
    for point in points:
        arr[point.y][point.x] = True
    out = ""
    empty = True
    for line in arr:
        for c in line:
            out += "#" if c else "."
        out +=  "\n"
    print(out)


def fold(points, fold):
    new_points = set()

    max_for_axis = max(getattr(p, fold.axis) for p in points) + 1
    print(max_for_axis)
    for point in points:
        axis_value = getattr(point, fold.axis)
        if max_for_axis // 2 > fold.value and axis_value < fold.value:
            print('case 1')
            new_value = axis_value + abs(axis_value - fold.value) * 2
            new_points.add(set_point_axis(point, fold.axis, new_value))
        elif max_for_axis // 2 < fold.value and axis_value > fold.value:
            print('case 2')
            new_value = axis_value - abs(axis_value - fold.value) * 2
            new_points.add(set_point_axis(point, fold.axis, new_value))
        else:
            new_points.add(point)
    
    return new_points


'''
hello ther
11 - (11 - 7) * 2
11 - (11 - 7) * 2
11 - 8
3
            7   
1 2 3 4 5 6 7 8 9 10 11
'''


print_points(POINTS)

for f in FOLDS:
    print(f)
    print_points(fold(POINTS, f))
    break

print(getattr(list(POINTS)[-1], 'x'), getattr(list(POINTS)[0], 'y'))
# print("p1:", len(fold(POINTS, FOLDS[0])))

