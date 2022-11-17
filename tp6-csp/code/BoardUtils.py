import random
import numpy


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


def is_consistent(board: [int | None], col: int, row: int) -> bool:
    """
    Checks if a given board will remain consistent after placing a queen in a given column and row.
    Only checks inconsistency with the values at the right starting from the given indexes, the remaining left values
    should be None.

    :param board: An array representing a partially filled chess board.
    :param col: The column index.
    :param row: The row index.
    :return: If that last movement was consistent.
    """
    n = len(board)

    # Row
    if row in board[:col]:
        return False  # Inconsistent

    # Diags
    for i in range(1, col + 1):
        if board[col - i] == row - i:
            return False  # Inconsistent main
        if board[col - i] == row + i:
            return False  # Inconsistent sec

    return True  # Consistent


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


class Board:
    def __init__(self, size):
        self.board = [None] * size
        self.domains = [[0 for _ in range(size)] for _ in range(size)]

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        # Fix domains
        if value is None:  # Emptying
            self.update_domain(key, self.board[key], inc=-1)
            self.board[key] = value
            return 0

        elif self.board[key] is not None:  # Overriding
            self.update_domain(key, self.board[key], inc=-1)

        # Assign and update
        self.board[key] = value
        self.update_domain(key, value)

    def update_domain(self, key, value, inc=1):
        n = len(self.board)

        # Row
        for domain in self.domains:
            domain[value] += inc

        # Main diagonal
        dc = key
        dr = value

        if dc > dr:
            dc -= dr
            dr = 0
        else:
            dr -= dc
            dc = 0

        d = max(dc, dr)
        for i in range(n - d):
            self.domains[dc + i][dr + i] += inc

        # Secondary diagonal
        dr = value - (n - 1 - key)
        dc = n - 1

        for i in range(max(0, -dr), n):
            if dr + i == n:
                break
            self.domains[dc - i][dr + i] += inc

        # Fix self domain over-assignation
        self.domains[key][value] -= 2 * inc

    def __get__(self, instance, owner):
        return self.board

    def __len__(self):
        return len(self.board)

    def __repr__(self):
        return repr(self.board)


def print_domains(bo):
    size = len(bo.domains)

    for col in range(size):
        for row in range(size):
            if bo.board[row] == col:
                print(f'\033[91m{bo.domains[row][col]}\033[00m ', end='')
            elif bo.domains[row][col] == 0:
                print(f'{bo.domains[row][col]} ', end='')
            else:
                print(f'\033[96m{bo.domains[row][col]}\033[00m ', end='')

        print("")
    print("\n")


def mrv_sort(board: Board):
    zeros = list(map(count_zeros, board.domains))

    min_idx = None
    min_value = None

    for i in range(len(board)):
        if board[i] is None and (min_idx is None or min_value > zeros[i]):
            min_idx = i
            min_value = zeros[i]

    return min_idx


def count_zeros(l: list):
    return sum(map(lambda x: (x == 0), l))


def main():
    size = 5
    B = Board(size)
    B[2] = 1
    B[1] = 4
    B[3] = 3
    B[0] = 2
    B[4] = 0

    print_domains(B)
    print(mrv_sort(B))


if __name__ == '__main__':
    main()
