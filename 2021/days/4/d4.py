# %%
import re
import numpy as np

def parse_input(path="./input"):
    with open(path) as f:
        text = f.read().strip()
    

    lines = text.split("\n")
    numbers = [*map(int, lines[0].strip().split(","))]
    boards_text = "\n".join(lines[2:]).strip().split("\n\n")
    
    boards = [parse_board(b) for b in boards_text]
    return numbers,boards

def parse_board(board_text):
    return np.array([parse_board_line(row) for row in board_text.split("\n")])

def parse_board_line(line: str):
    line = line.strip()
    line = re.sub("\s+", " ", line)
    return tuple(map(int, line.split(" ")))

numbers, boards = parse_input("input")




def get_num_coords(number, board):
    return tuple(zip(*np.where(board==number)))
    

def find_final_score():
    seen = set()
    for i, number in map(np.int64, numbers):
        seen.add(number)
        for board in boards:
            coords = get_num_coords(number, board)
            for coord in coords:
                is_winning_row = all(n in seen for n in  board[coord[0], :])
                is_winning_col = all(n in seen for n in  board[:, coord[1]])
                if is_winning_row or is_winning_col:
                    seen_inv_masked_sum = sum(n for n in board.flatten() if not n in seen)
                    return seen_inv_masked_sum * number                
    

print(boards[0])
find_final_score()
# %% p2

def find_last_board_win_final_score():
    seen = set()
    winning_already = set()
    board_count = len(boards)
    
    i_boards = list(enumerate(boards))
    for number in map(np.int64, numbers):
        seen.add(number)
        for b_index, board in filter(lambda e: not e[0] in winning_already, i_boards):
            print("trying ", b_index)
            coords = get_num_coords(number, board)
            for coord in coords:
                is_winning_row = all(n in seen for n in  board[coord[0], :])
                is_winning_col = all(n in seen for n in  board[:, coord[1]])
                if is_winning_row or is_winning_col:
                    print(b_index, "won!")
                    winning_already.add(b_index)
                    if len(winning_already) >= board_count:
                        seen_inv_masked_sum = sum(n for n in board.flatten() if not n in seen)
                        return seen_inv_masked_sum * number

find_last_board_win_final_score()
