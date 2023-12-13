R = []
with open('days/2/input_d2.txt') as f:
    for line in f:
        R.append(list(map(int, line.strip().split())))

def p1():
    num_valid = 0
    for rep in R:
        dir = 1 if rep[0] < rep[1] else -1
        for i in range(1, len(rep)):
            diff = rep[i] - rep[i-1]
            if diff == 0 or diff // abs(diff) != dir:
                break
            if abs(diff) < 1 or abs(diff) > 3:
                break
        else:
            num_valid += 1
    print("p1", num_valid)


def p2():
    num_valid = 0
    for rep in R:
        tally = 0
        for i in range(1,len(rep)):
            a = rep[i - 1]
            b = rep[i]
            if a == b:
                continue
            if a < b:
                tally += 1
            else:
                tally -= 1

        if tally == 0:
            continue
        dir = tally // abs(tally)

        if dir == -1:
            rep = [*reversed(rep)]

        attempts = [rep]
        while attempts:
            curr = attempts.pop()
            for i in range(1, len(curr)):
                a = curr[i-1]
                b = curr[i]
                if (b - a) > 3 or (b-a) <= 0:
                    break
            else:
                num_valid += 1
                break
            if rep is curr:
                attempts = [
                    curr[:i-1] + curr[i:],
                    curr[:i] + curr[i+1:]
                ]

    print("p2", num_valid)



if __name__ == '__main__':
    p1()
    p2()
