import math
import random
from BoardUtils import h, h_fast, board_to_str


def hill_climbing(board: list, max_steps):
    """
    Will
    :param board: The board to be analyzed, In-Place
    :param max_steps: The maximum amount of states to explore. (Verified once per iteration).
    """
    n = len(board)
    best_value = h(board)
    h_history = [best_value]
    steps = 0

    # Hill climbing
    while best_value != 0 and steps < max_steps:
        # Best neighbor
        better_neighbors = []

        # Try each column and row
        for col in range(n):
            for row in range(n):
                # Skip current state
                if row == board[col]:
                    continue

                # Evaluate
                value = h_fast(board, col, row, best_value)

                # Verify if better
                if value < best_value:
                    better_neighbors.append((value, col, row))

        # Register steps
        steps += n * n - n

        # Check results
        if better_neighbors:
            best_value, col, row = random.choice(better_neighbors)
            h_history.append(best_value)
            board[col] = row
        else:
            break

    # Return
    return best_value, steps, h_history


if __name__ == '__main__':
    random.seed()
    sizes = [4, 8, 10]
    algorithms = [hill_climbing]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            board = random.sample(range(size), size)
            best_h, steps, _ = algorithm(board, math.inf)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')
