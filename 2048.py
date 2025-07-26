import random
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    clear_screen()
    print("-" * 21)
    for row in board:
        print("|", end="")
        for num in row:
            if num == 0:
                print("    .", end="|")
            else:
                print("{:5d}".format(num), end="|")
        print("\n" + "-" * 21)
    print()

def init_board():
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_new(board)
    add_new(board)
    return board

def add_new(board):
    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty:
        return
    i, j = random.choice(empty)
    board[i][j] = 2 if random.random() < 0.9 else 4

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def merge(row):
    for i in range(3):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    return row

def move_left(board):
    moved = False
    new_board = []
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        compressed = compress(merged)
        if compressed != row:
            moved = True
        new_board.append(compressed)
    return new_board, moved

def move_right(board):
    moved = False
    new_board = []
    for row in board:
        reversed_row = row[::-1]
        compressed = compress(reversed_row)
        merged = merge(compressed)
        compressed = compress(merged)
        compressed = compressed[::-1]
        if compressed != row:
            moved = True
        new_board.append(compressed)
    return new_board, moved

def move_up(board):
    moved = False
    new_board = [[0]*4 for _ in range(4)]
    for col in range(4):
        col_vals = [board[row][col] for row in range(4)]
        compressed = compress(col_vals)
        merged = merge(compressed)
        compressed = compress(merged)
        for row in range(4):
            new_board[row][col] = compressed[row]
            if new_board[row][col] != board[row][col]:
                moved = True
    return new_board, moved

def move_down(board):
    moved = False
    new_board = [[0]*4 for _ in range(4)]
    for col in range(4):
        col_vals = [board[row][col] for row in range(4)][::-1]
        compressed = compress(col_vals)
        merged = merge(compressed)
        compressed = compress(merged)
        compressed = compressed[::-1]
        for row in range(4):
            new_board[row][col] = compressed[row]
            if new_board[row][col] != board[row][col]:
                moved = True
    return new_board, moved

def can_move(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return True
            if j < 3 and board[i][j] == board[i][j+1]:
                return True
            if i < 3 and board[i][j] == board[i+1][j]:
                return True
    return False

def main():
    board = init_board()
    while True:
        print_board(board)
        move = input("Use WASD or Arrow keys to move (q to quit): ").lower()
        if move in ['a', '\x1b[D']:  # left
            board, moved = move_left(board)
        elif move in ['d', '\x1b[C']:  # right
            board, moved = move_right(board)
        elif move in ['w', '\x1b[A']:  # up
            board, moved = move_up(board)
        elif move in ['s', '\x1b[B']:  # down
            board, moved = move_down(board)
        elif move == 'q':
            print("Bye!")
            sys.exit()
        else:
            continue

        if moved:
            add_new(board)
            if not can_move(board):
                print_board(board)
                print("Game Over!")
                break

if __name__ == "__main__":
    main()
