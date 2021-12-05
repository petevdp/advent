import numpy as np


def parse_input(path="./input"):
    with open(path) as f:
        text = f.read().strip()

    numbers, *boards = [l for l in text.split("\n\n")]
    numbers = [np.int64(n) for n in numbers.strip().split(",")]
    boards = [parse_board(b) for b in boards]
    return numbers, boards


def parse_board(board_text):
    return np.array([parse_board_row(n) for n in board_text.split("\n")])


def parse_board_row(row: str):
    return tuple(map(int, row.split()))


def get_num_coords(number, board):
    return tuple(zip(*np.where(board == number)))


numbers, boards = parse_input("input")


def gen_winning_scores():
    seen = set()
    winning_boards = set()

    for number in map(np.int64, numbers):
        seen.add(number)
        for b_index, board in enumerate(boards):
            if b_index in winning_boards:
                continue
            for coord in get_num_coords(number, board):
                is_winning_row = all(n in seen for n in board[coord[0], :])
                is_winning_col = all(n in seen for n in board[:, coord[1]])
                if is_winning_row or is_winning_col:
                    winning_boards.add(b_index)
                    seen_inv_masked_sum = sum(
                        n for n in board.flatten() if not n in seen)
                    yield seen_inv_masked_sum * number


scores = [*gen_winning_scores()]
print("p1: ", scores[0])
print("p2: ", scores[-1])
