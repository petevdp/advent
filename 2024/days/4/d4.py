import sys

input_file = sys.argv[1]


T = list("XMAS")
S = []
with open(input_file) as f:
    for line in f:
        if not line.strip():
            continue
        SL = []
        S.append(SL)
        for char in line.strip():
            SL.append(char)
width = len(S[0])
height = len(S)

def part1():
    count = 0
    for i in range(height):
        for j in range(width):
            horizontal = S[i][j:j + len(T)]
            if horizontal == T or horizontal == T[::-1]:
                count += 1

            vertical = [c[j] for c in S[i:i + len(T)]]
            if vertical == T or vertical == T[::-1]:
                count += 1

            if (i >= height - (len(T) - 1) or j >= width - (len(T) - 1)):
                continue
            diag1 = []
            diag2 = []
            for k in range(len(T)):
                diag1.append(S[i + k][j + k])
                diag2.append(S[i + k][j + (len(T) - 1) - k])
            if diag1 == T or diag1 == T[::-1]:
                count += 1
            if diag2 == T or diag2 == T[::-1]:
                count += 1
    print("p1", count)


M = list("MAS")
def part2():
    count = 0
    for i in range(height - 2):
        for j in range(width - 2):
            diag1 = []
            diag2 = []
            for k in range(3):
                diag1.append(S[i + k][j + k])
                diag2.append(S[i + k][j + 2 - k])

            if (diag1 == M or diag1 == M[::-1]) and (diag2 == M or diag2 == M[::-1]):
                count += 1
    print("p2", count)



if __name__ == '__main__':
    part1()
    part2()
