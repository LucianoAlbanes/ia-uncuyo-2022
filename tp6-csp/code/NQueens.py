from BoardUtils import h, board_to_str, isConsistent


def backtracking(size: int):
    # Only backtrack, without heuristics. Checks for consistency in each step.

    def _backtrack(col=0):
        nonlocal iterations

        # General case
        for value in range(size):  # Test each value in domain
            if isConsistent(board, col, value):  # If the value is consistent, assign it
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


if __name__ == '__main__':
    sizes = [4, 8, 10, 12, 15]
    algorithms = [backtracking]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            # Run and print results
            board, best_h, steps = algorithm(size)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')
