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


# def h(board):
#     # This functions calculates the pairs of queens under attack across the board.
#
#     attacked_pairs = 0
#     n = len(board)
#     # Columns not needed, problem relaxed, one queen per column.
#
#     # Rows
#     for col in range(n):
#         for i in range(col + 1, n):
#             if board[col] == board[i]:
#                 attacked_pairs += 1
#
#     # Main Diagonals
#     for col in range(n - 1):
#         for i in range(1, min(n - board[col] - 1, n - col - 1)):
#             if board[col] + i == board[col + i]:
#                 attacked_pairs += 1
#
#     # Secondary diagonals
#     for col in range(n):
#         for i in range(1, min(n - board[col], col + 1)):
#             if board[col] + i == board[col - i]:
#                 attacked_pairs += 1
#
#     return attacked_pairs


def h(board):
    # This functions calculates the pairs of queens under attack ACROSS the board.
    attacked_pairs = 0

    # Note: could parallelize
    for col in range(len(board)):
        attacked_pairs += calc_rows(board, col)
        attacked_pairs += calc_main_diag(board, col)
        attacked_pairs += calc_sec_diag(board, col)

    return attacked_pairs


def h_fast(board, col, pos, h_prev):
    # Need fixing - Don't use

    # This function calculates the pairs on queens under attack across the board, after a given movement in ONE queen.
    # The calculation in a lot cheaper than h(), because only checks involved queens after the movement.
    # To perform this calculation, is required the previous number of queens under attack.

    # Some variables
    original_pos = board[col]
    n = len(board)
    involved_before = 0
    involved_after = 0

    # Before
    # Row
    for i in range(n):
        if board[i] == board[col]:
            involved_before += calc_rows(board, i)

    # Main diag
    d = max(col - board[col], board[col] - col)
    for i in range(n-d):
        if d+i == board[i]:
            involved_before += calc_main_diag(board, i)

    # Secondary diag
    d = min(n - col -1, 999)
    for i in range(d):  # 0-3
        if d-i == board[d-i]:
            involved_before += calc_sec_diag(board, 3)

    # After
    board[col] = pos
    # Row
    for i in range(n):
        if board[i] == board[col]:
            involved_after += calc_rows(board, i)

    # Main diag
    d = max(col - board[col], board[col] - col)
    for i in range(n-d):
        if d+i == board[i]:
            involved_after += calc_main_diag(board, i)

    # Secondary diag
    d = min(col + board[col], board[col])
    for i in range(n - d):  # 0-3
        if board[col] + i == board[col - i]:
            involved_after += calc_sec_diag(board, i+d)

    # Rollback changes
    board[col] = original_pos

    return h_prev - involved_before + involved_after


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


def hill_climbing(board, max_steps, goal_fn=h):
    n = len(board)
    best_value = goal_fn(board)
    steps = 0

    # Hill climbing
    while best_value != 0 and steps < max_steps:
        # Best neighbor
        better_neighbors = []

        # Try each column and row
        for col in range(n):
            tmp = board[col]    # Save the original value
            for row in range(n):
                steps += 1

                # Skip current state
                if row == tmp:
                    continue

                # Move and evaluate
                board[col] = row
                value = goal_fn(board)

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


if __name__ == '__main__':
    k = 8
    b = random.sample(range(k), k)
    h_reached, b, steps = hill_climbing(b, math.inf, h)
    # print(f'{b=}, {h_reached=}')
    # print(str_board(b))

    solutions = set()
    for i in range(100*k):
        random.shuffle(b)
        h_reached, b, steps = hill_climbing(b, math.inf, h)

        while h_reached > 0:
            random.shuffle(b)
            h_reached, b, steps = hill_climbing(b, math.inf, h)

        solutions.add(tuple(b))

    print(solutions)
    print(len(solutions))
