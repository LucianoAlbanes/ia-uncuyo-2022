import math
import random
from BoardUtils import h, h_fast, board_to_str


def hill_climbing(board: list, max_steps):
    """
    :param board: The board to be analyzed, In-Place
    :param max_steps: The maximum amount of states to explore. (Verified once per iteration).
    """
    n = len(board)
    best_value = h(board)
    h_history = [(0, best_value)]
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
            h_history.append((steps, best_value))
            board[col] = row
        else:
            break

    # Return
    return best_value, steps, h_history


def simulated_annealing(board: list, max_iterations):
    """
    :param board: The board to be analyzed, In-Place
    :param max_iterations: The maximum amount of iterations to perform
    """

    n = len(board)
    best_value = h(board)
    h_history = [(0, best_value)]
    iterations = 0
    memo = dict()

    # Simulated Annealing
    for time in range(max_iterations):
        # Temp function
        temp = 1/(time+1)

        # Can't anneal
        if best_value == 0:
            break

        # Register iterations
        iterations += 1

        # Get random successor
        col = random.randint(0, n-1)
        row = random.randint(0, n-1)
        try:
            value = memo[(col, row)]
        except KeyError:
            value = h_fast(board, col, row, best_value)

        # Get delta
        delta = value - best_value

        # Choose new value if improves OR probability
        if delta < 0 or (random.uniform(0, 1) <= math.exp(-delta / temp)):
            best_value = value
            board[col] = row
            h_history.append((iterations, best_value))
            memo.clear()
        else:
            # Save memo
            memo[(col, row)] = value

    # Return
    return best_value, iterations, h_history


if __name__ == '__main__':
    sizes = [4, 8, 10]
    algorithms = [hill_climbing, simulated_annealing]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            board = random.sample(range(size), size)
            best_h, steps, hi = algorithm(board, size**10)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')
