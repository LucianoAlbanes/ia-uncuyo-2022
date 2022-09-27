import math
import random
from BoardUtils import h, h_fast, board_to_str


def hill_climbing(size: int, max_iterations: int):
    # Variables
    best_board = random.sample(range(size), size)
    best_value = h(best_board)
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
                if row == best_board[col]:
                    continue

                # Evaluate
                value = h_fast(best_board, col, row, best_value)

                # Verify if better
                if value < best_value:
                    better_neighbors.append((value, col, row))

        # Register iterations
        iterations += size * size - size

        # Check results
        if better_neighbors:
            best_value, col, row = random.choice(better_neighbors)
            h_history.append((iterations, best_value))
            best_board[col] = row
        else:
            break

    # Return
    return best_board, best_value, iterations, h_history


def simulated_annealing(size: int, max_iterations: int, init_temp=700, alpha=0.95):
    # Variables
    best_board = random.sample(range(size), size)
    best_value = h(best_board)
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
            value = h_fast(best_board, col, row, best_value)

        # Get delta
        delta = value - best_value

        # Choose new value if improves OR probability
        if delta < 0 or (random.uniform(0, 1) <= math.exp(-delta / temp)):
            best_value = value
            best_board[col] = row
            h_history.append((iterations, best_value))
            memo.clear()
        else:
            # Save memo
            memo[(col, row)] = value

    # Return
    return best_board, best_value, iterations, h_history


def genetic_algorithm(size: int, max_iterations: int, population_size=50, mutation_rate=0.05):
    # Population must be divisible by 2
    if population_size % 2 != 0:
        population_size += 1

    # Variables
    iterations = population_size
    fit_objetive = int((size - 1) * size / 2)
    h_history = []

    # Generate random population and calculate fitness (h)
    population = [random.sample(range(size), size) for _ in range(population_size)]
    population_tuples = sorted([((fit_objetive - h(board)), board) for board in population], reverse=True)

    population = [None]*population_size
    population_h = [0]*population_size
    for i in range(population_size):
        population_h[i], population[i] = population_tuples[i]

    # Save initial best board
    best_board = population[0]
    best_value = population_h[0]
    h_history.append((0, fit_objetive - best_value))

    # Genetic Algorithm
    # Run iterations
    while best_value < fit_objetive and iterations < max_iterations:
        new_population = []
        for _ in range(int(population_size/2)):
            # Select two random parents, weighted by non-attacking queens
            p1, p2 = None, None
            while p1 is p2:
                selected = random.choices(population, population_h, k=2)
                p1 = selected[0]
                p2 = selected[1]

            # Crossover by Order 1
            # Select cutting points and copy from parents
            cutA, cutB = None, None
            while cutA is cutB:
                cutA = random.randint(0, size-2)
                cutB = random.randint(cutA, size-1)

            partA = [None]*cutA
            partB = [None]*(size-cutB)

            children = [
                partA + p1[cutA:cutB] + partB,
                partA + p2[cutA:cutB] + partB
            ]

            # Finish copying from other parent
            for child in children:
                for i in range(size):
                    index = (i+cutB) % size

                    if index == cutA:
                        break
                    elif p1[index] not in child:
                        child[index] = p1[index]

                # Swap parents to work with the other child
                tmp = p1
                p1 = p2
                p2 = tmp

            # Mutation and save
            for child in children:
                if random.uniform(0, 1) >= mutation_rate:
                    # Swap two queens
                    v1, v2 = random.randint(0, size-1), random.randint(0, size-1)
                    while v1 == v2:
                        v1, v2 = random.randint(0, size - 1), random.randint(0, size - 1)

                    tmp = child[v1]
                    child[v1] = child[v2]
                    child[v2] = tmp

                # Save to population
                new_population.append(child)

        # Update population
        # Calculate and sort children by fittness
        new_population_tuples = sorted([((fit_objetive - h(child)), child) for child in new_population])
        successor = new_population_tuples.pop()

        # Replace in original population
        for i in range(population_size):
            # Compare with current population at i
            if population_h[i] < successor[0]:
                # Replace board
                population_h[i] = successor[0]
                population[i] = successor[1]

                # Check if is a new best solution
                if population_h[i] > best_value:
                    best_board = population[i]
                    best_value = population_h[i]

                # Get new successor
                try:
                    successor = new_population_tuples.pop()
                except IndexError:
                    break

        # Increment iterations count and update history
        iterations += population_size
        h_history.append((iterations, fit_objetive - best_value))

    # Return best solution found
    return best_board, (fit_objetive-best_value), iterations, h_history


if __name__ == '__main__':
    sizes = [4, 8, 10]
    algorithms = [hill_climbing, simulated_annealing, genetic_algorithm]

    for algorithm in algorithms:
        print(f'~~~Algorithm: {algorithm.__name__}~~~')
        for size in sizes:
            # Run and print results
            board, best_h, steps, hi = algorithm(size, size**4)
            print(f'{size= }, {best_h= }, {steps= }, {board= }\n{board_to_str(board)}\n')
