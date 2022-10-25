from BoardUtils import h, board_to_str, is_consistent, Board


def backtracking(size: int):
    # Only backtrack, without heuristics. Checks for consistency in each step.

    def _backtrack(col=0):
        nonlocal iterations

        # General case
        for value in range(size):  # Test each value in domain
            if is_consistent(board, col, value):  # If the value is consistent, assign it
                iterations += 1
                board[col] = value  # Assign
                if col + 1 == size or _backtrack(col + 1):  # Test for solution, or backtrack
                    return True

    # Variables
    board = [None] * size
    iterations = 0

    # Start backtrack
    _backtrack()

    # Return
    return board, h(board), iterations


def forwardchecking(size: int):
    # Only backtrack, without heuristics. Checks for consistency in each step.

    def _backtrack(col=0):
        nonlocal iterations

        # General case
        for value in range(size):  # Test each value in domain
            if is_consistent(board, col, value):  # If the value is consistent, assign it
                iterations += 1
                board[col] = value  # Assign

                # Verify if all domains have at least one free value.
                fw_check_pass = True
                for i, domain in enumerate(board.domains):
                    if board[i] is None and 0 not in domain:
                        fw_check_pass = False
                        break

                # Test for solution, or backtrack
                if fw_check_pass and (col + 1 == size or _backtrack(col + 1)):
                    return True

                # Undo assignation
                board[col] = None

    # Variables
    board = Board(size)
    iterations = 0

    # Start backtrack
    _backtrack()

    return board, h(board), iterations


def main():
    sizes = [4, 8, 10, 12, 15]
    algorithms = [backtracking, forwardchecking]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            # Run and print results
            board, best_h, steps = algorithm(size)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')


if __name__ == '__main__':
    main()
