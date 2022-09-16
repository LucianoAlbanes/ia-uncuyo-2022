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

def h_fast(board, col, row, h_prev):
    # This function calculates the pairs on queens under attack across the board, after a given movement of ONE queen.
    # The calculation in a lot cheaper than h(), because only checks involved queens after the movement.
    # To perform this calculation, is required the previous number of queens under attack.
    # Will roll back changes in board
    # Its horrible, but should work. There is a bruteforce test.

    def delta():
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

        if dc > dr:
            dc -= dr
            dr = 0
        else:
            dr -= dc
            dc = 0

        d = max(dc, dr)
        for i in range(n - d):
            if dr + i == board[dc + i]:
                counter += calc_main_diag(board, dc + i)
                break

        # Secondary diagonal
        dr = board[col] - (n - 1 - col)
        dc = n - 1

        for i in range(n - dr):
            if dr + i == board[dc - i]:
                counter += calc_sec_diag(board, dc - i)
                break

        # Return
        return counter

    # Save original row position
    original_pos = board[col]

    # Before
    involved_before = delta()

    # After
    board[col] = row
    involved_after = delta()

    # Rollback changes
    board[col] = original_pos

    # Return calculated value
    return h_prev - involved_before + involved_after


def board_to_str(board):
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

    print(board_to_str(board))
    print(f'{h(board)=}, {fast=}')
