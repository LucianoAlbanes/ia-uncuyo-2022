import math
import random
from BoardUtils import h, h_fast, board_to_str


def hill_climbing(size: int, max_iterations: int):
    # Variables
    board = random.sample(range(size), size)
    best_value = h(board)
    h_history = [(0, best_value)]
    iterations = 0

    # Hill climbing
    while best_value != 0 and iterations < max_iterations:
        # Best neighbor
        better_neighbors = []

        # Try each column and row
        for col in range(size):
            for row in range(size):
                # Skip current state
                if row == board[col]:
                    continue

                # Evaluate
                value = h_fast(board, col, row, best_value)

                # Verify if better
                if value < best_value:
                    better_neighbors.append((value, col, row))

        # Register iterations
        iterations += size * size - size

        # Check results
        if better_neighbors:
            best_value, col, row = random.choice(better_neighbors)
            h_history.append((iterations, best_value))
            board[col] = row
        else:
            break

    # Return
    return board, best_value, iterations, h_history


def simulated_annealing(size: int, max_iterations: int, init_temp=700, alpha=0.95):
    # Variables
    board = random.sample(range(size), size)
    best_value = h(board)
    h_history = [(0, best_value)]
    temp = init_temp
    iterations = 0
    memo = {}

    # Simulated Annealing
    for time in range(max_iterations):
        # Temp function (geometric schedule)
        temp *= alpha

        # Can't anneal
        if best_value == 0:
            break

        # Register iterations
        iterations += 1

        # Get random successor
        col = random.randint(0, size-1)
        row = random.randint(0, size-1)
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
    return board, best_value, iterations, h_history


def genetic_algorithm(size: int, max_iterations: int, population_size=1000, mutation_rate=0.75):
    # Population must be divisible by 2
    if population_size % 2 != 0:
        population_size += 1

    # Variables
    iterations = population_size
    fit_objetive = int((size - 1) * size / 2)
    board = []
    best_value = 0
    h_history = []

    # Generate random population and calculate fitness (h)
    population = [random.sample(range(size), size) for _ in range(population_size)]
    population_h: list[int] = [0] * population_size
    for i in range(population_size):
        fitness = fit_objetive - h(population[i])

        # Check if better solution was found
        if fitness > best_value:
            board = population[i]
            best_value = fitness

        # Append to weights list
        population_h[i] = fitness
    h_history.append((0, fit_objetive - best_value))

    # Genetic Algorithm
    # Run iterations
    while best_value < fit_objetive and iterations < max_iterations:
        new_population = []
        for _ in range(int(population_size/2)):
            # Select two random parents, weighted by non-attacking queens
            x, y = None, None
            while x is y:
                selected = random.choices(population, population_h, k=2)
                x = selected[0]
                y = selected[1]

            # Crossover
            cut = random.randint(1, size-2)
            children = [
                x[0:cut] + y[cut:size],
                y[0:cut] + x[cut:size]
            ]

            # Mutation and save to new_population
            for child in children:
                if random.uniform(0, 1) >= mutation_rate:
                    child[random.randint(0, size-1)] = random.randint(0, size-1)
                new_population.append(child)

        # Update new population
        population = new_population
        for i in range(population_size):
            fitness = fit_objetive - h(population[i])

            # Check if better solution was found
            if fitness > best_value:
                board = population[i]
                best_value = fitness

            # Append to weights list
            population_h[i] = fitness

        # Increment iterations count and update history
        iterations += population_size
        h_history.append((iterations, fit_objetive - best_value))

    # Return best solution found
    return board, (fit_objetive-best_value), iterations, h_history


if __name__ == '__main__':
    sizes = [4, 8, 10, 30]
    algorithms = [hill_climbing, simulated_annealing, genetic_algorithm]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            # Run and print results
            board, best_h, steps, hi = algorithm(size, size**4)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')
