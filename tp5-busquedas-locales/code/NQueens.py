import math
import random


def calc_main_diag(board, col):
    attacked_pairs = 0
    n = len(board)

    for i in range(1, min(n - board[col], n - col)):
        if board[col] + i == board[col + i]:
            attacked_pairs += 1

    return attacked_pairs


def calc_sec_diag(board, col):
    attacked_pairs = 0
    n = len(board)

    for i in range(1, min(n - board[col], col + 1)):
        if board[col] + i == board[col - i]:
            attacked_pairs += 1

    return attacked_pairs


def calc_rows(board, col):
    attacked_pairs = 0
    n = len(board)

    for row in range(col + 1, n):
        if board[col] == board[row]:
            attacked_pairs += 1
    return attacked_pairs


def h(board):
    # This functions calculates the pairs of queens under attack ACROSS the board.
    # Only use if needed, there is a h_fast() function bellow.
    attacked_pairs = 0

    # Note: could parallelize
    for col in range(len(board)):
        attacked_pairs += calc_rows(board, col)
        attacked_pairs += calc_main_diag(board, col)
        attacked_pairs += calc_sec_diag(board, col)

    return attacked_pairs


def h_fast(board, col, pos, h_prev):
    # This function calculates the pairs on queens under attack across the board, after a given movement in ONE queen.
    # The calculation in a lot cheaper than h(), because only checks involved queens after the movement.
    # To perform this calculation, is required the previous number of queens under attack.
    # Its horrible, but should work. There is a bruteforce test.

    # Some variables
    original_pos = board[col]
    n = len(board)

    # Before
    involved_before = delta(board, col)

    # After
    board[col] = pos
    involved_after = delta(board, col)

    # Rollback changes
    board[col] = original_pos

    # Return calculated value
    return h_prev - involved_before + involved_after


def delta(board, col):
    n = len(board)
    counter = 0

    # Row
    for i in range(n):
        if board[i] == board[col]:
            counter += calc_rows(board, i)
            break

    # Main diagonal
    dc = col
    dr = board[col]

    while dc != 0 and dr != 0:
        dc -= 1
        dr -= 1

    d = max(dc, dr)
    for i in range(n - d):
        if dr+i == board[dc + i]:
            counter += calc_main_diag(board, dc + i)
            break

    # Secondary diagonal
    dc = col
    dr = board[col]

    while dc != n-1 and dr != 0:
        dc += 1
        dr -= 1

    d = max(dc, dr, 1)
    for i in range(n - dr):
        if dr+i == board[d-i]:
            counter += calc_sec_diag(board, d-i)
            break

    # Return
    return counter


def str_board(board):
    txt = ''
    n = len(board)
    for i in range(n):
        for j in range(n):
            if i == board[j]:
                txt += 'Q '
            else:
                txt += '_ '
        txt += '\n'
    return txt


def hill_climbing(board, max_steps):
    n = len(board)
    best_value = h(board)
    steps = 0

    # Hill climbing
    while best_value != 0 and steps < max_steps:
        # Best neighbor
        better_neighbors = []

        # Try each column and row
        for col in range(n):
            tmp = board[col]
            for row in range(n):
                steps += 1

                # Skip current state
                if row == tmp:
                    continue

                # Evaluate
                value = h_fast(board, col, row, best_value)

                # Verify if better
                if value < best_value:
                    better_neighbors.append((value, col, row))

            # Rollback to original row
            board[col] = tmp

        # Check results
        if better_neighbors:
            best_value, col, row = random.choice(better_neighbors)
            board[col] = row
        else:
            break

    return best_value, board, steps


def bruteforce_fast_h(size):
    count = 0
    while True:
        board = random.sample(range(size), size)
        a = random.randint(0, size - 1)
        b = random.randint(0, size - 1)

        # Real queens under attack (expensive)
        base = h(board)

        # calc h using h_fast. Moves queen at col 'a' to row 'b'
        fast = h_fast(board, a, b, base)

        # calc same movement, but expensive
        board[a] = b

        # Break if fails
        if fast != h(board):
            break
        count += 1
        print(count)

    print(str_board(board))
    print(f'{h(board)=}, {fast=}')


if __name__ == '__main__':
    # k = 8
    # b = random.sample(range(k), k)
    # h_reached, b, steps = hill_climbing(b, math.inf)
    # # print(f'{b=}, {h_reached=}')
    # # print(str_board(b))
    #
    # solutions = set()
    # for i in range(10*k):
    #     random.shuffle(b)
    #     h_reached, b, steps = hill_climbing(b, math.inf)
    #
    #     while h_reached > 0:
    #         random.shuffle(b)
    #         h_reached, b, steps = hill_climbing(b, math.inf)
    #
    #     solutions.add(tuple(b))
    #
    # print(solutions)
    # print(len(solutions))
    bruteforce_fast_h(100)
