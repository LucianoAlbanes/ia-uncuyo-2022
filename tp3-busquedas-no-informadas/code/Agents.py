import random
from enum import Enum, auto

from lib.Queues import Queue, Stack, PriorityQueue


# noinspection PyArgumentList
class SLOT(Enum):
    EMPTY = auto()
    OBSTRUCTED = auto()
    INITIAL_POS = auto()
    GOAL_POS = auto()


# Functions
def access_matrix(matrix: list, vector: tuple):
    prev = matrix
    for i in vector:
        prev = prev[i]
    return prev


def set_matrix(matrix: list, vector: tuple, value: SLOT):
    prev = matrix
    for i in range(len(vector) - 1):
        prev = prev[vector[i]]
    prev[vector[-1]] = value


def sum_pos(a: tuple, b: tuple):
    return a[0] + b[0], a[1] + b[1]


# Def Classes
class Environment:
    __slots__ = ('shape', 'init_pos', 'goal_pos', 'grid', 'obstacle_rate')

    def __init__(self, shape: tuple, init_pos: tuple, goal_pos: tuple, obstacle_rate: float):
        # Size
        if min(shape) <= 0:
            raise Exception('All dimensions sizes must be positive.')
        self.shape = shape

        # Init pos (Verifies: 1. Same # of dimensions, 2. All init_pos must be positive 3. Valid init_pos in each dim.
        if not self.is_valid_pos(init_pos):
            raise Exception('Illegal initial position.')
        self.init_pos = init_pos

        # Goal pos (same checks as init_pos)
        if not self.is_valid_pos(goal_pos):
            raise Exception('Illegal goal position.')
        self.goal_pos = goal_pos

        # Obstacle rate
        if obstacle_rate < 0 or obstacle_rate > 1:
            raise Exception('Obstacle rate must be between 0 and 1.')
        self.obstacle_rate = obstacle_rate

        # Proceed to initialize the grid
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        def _obstruct() -> SLOT:
            return SLOT.OBSTRUCTED if random.random() < self.obstacle_rate else SLOT.EMPTY

        def _gen_dims(depth=1):
            if depth == len(self.shape):
                return [_obstruct() for _ in range(self.shape[depth - 1])]
            else:
                return [_gen_dims(depth + 1) for _ in range(self.shape[depth - 1])]

        # Generate matrix
        self.grid = _gen_dims()

        # Clear init and goal positions. Could have been obstructed
        set_matrix(self.grid, self.init_pos, SLOT.INITIAL_POS)
        set_matrix(self.grid, self.goal_pos, SLOT.GOAL_POS)

    def __str__(self) -> str:
        # Only implemented for 1D and 2D grids
        def _colorize(x):
            match x:
                case SLOT.EMPTY:
                    return ' '
                case SLOT.OBSTRUCTED:
                    return 'X'
                case SLOT.INITIAL_POS:
                    return 'S'
                case SLOT.GOAL_POS:
                    return "G"

        txt = ''
        match len(self.shape):
            case 1:
                txt += str([_colorize(x) for x in self.grid]) + '\n'
            case 2:
                row: tuple  # Var hint
                for row in self.grid:
                    txt += str(([_colorize(x) for x in row])) + '\n'
            case _:
                raise NotImplementedError('Method only available for 1D and 2D environments')

        return txt

    def is_valid_pos(self, pos: tuple):
        return len(self.shape) == len(pos) and min(pos) >= 0 and False not in [(a > b) for a, b in zip(self.shape, pos)]


class GoalBasedAgent2D:
    __slots__ = ('env', 'explored_states')

    def __init__(self, env: Environment):
        self.env = env
        self.explored_states = 0

    def think(self):
        pass

    def _parse_path(self, discovered: dict) -> list:
        pos = self.env.goal_pos
        path = [pos]
        while (pos := discovered[pos]) != self.env.init_pos and pos:
            path.append(pos)

        path.reverse()
        return path

    def _get_borders(self, actual, discovered):
        # Possible directions
        candidates = [
            sum_pos(actual, (-1, 0)),  # UP
            sum_pos(actual, (1, 0)),  # DOWN
            sum_pos(actual, (0, 1)),  # RIGHT
            sum_pos(actual, (0, -1))  # LEFT
        ]

        # Checks for valid movements and not in discovered
        borders = []
        for candidate in candidates:
            if self.env.is_valid_pos(candidate) \
                    and access_matrix(self.env.grid, candidate) is not SLOT.OBSTRUCTED \
                    and candidate not in discovered:
                # New valid frontier node
                borders.append(candidate)

        # Return the list of valid border positions
        return borders


class GoalAgentBFS(GoalBasedAgent2D):
    def __init__(self, env: Environment):
        super(GoalAgentBFS, self).__init__(env)

    def think(self) -> list:
        # Init queue and discovered dict (hashed)
        frontier = Queue()
        frontier.push(self.env.init_pos)
        discovered = {self.env.init_pos: None}  # And save parents

        # BFS main
        while len(frontier) > 0:
            # Prepare actual state
            actual = frontier.pop()  # FIFO
            self.explored_states += 1

            # Verify if goal is reached
            if actual == self.env.goal_pos:
                return self._parse_path(discovered)
            else:
                borders = self._get_borders(actual, discovered)
                for border in borders:
                    frontier.push(border)
                    discovered[border] = actual

        # Return failure -> empty path
        return []


class GoalAgentDFS(GoalBasedAgent2D):
    def __init__(self, env: Environment):
        super(GoalAgentDFS, self).__init__(env)

    def think(self) -> list:
        # Init queue and discovered dict (hashed)
        frontier = Stack()
        frontier.push(self.env.init_pos)
        discovered = {self.env.init_pos: None}  # And save parents

        # DFS main
        while len(frontier) > 0:
            # Prepare actual state
            actual = frontier.pop()  # LIFO
            self.explored_states += 1

            # Verify if goal is reached
            if actual == self.env.goal_pos:
                return self._parse_path(discovered)
            else:
                borders = self._get_borders(actual, discovered)
                for border in borders:
                    frontier.push(border)
                    discovered[border] = actual

        # Return failure -> empty path
        return []


class GoalAgentDLS(GoalBasedAgent2D):
    def __init__(self, env: Environment, max_depth):
        super(GoalAgentDLS, self).__init__(env)
        self.max_depth = max_depth

    def think(self) -> list:
        # Init queue and discovered dict (hashed)
        frontier = Stack()
        frontier.push(self.env.init_pos)
        discovered = {self.env.init_pos: None}  # And save parents
        depths = {}

        # DLS main
        while len(frontier) > 0:
            # Prepare actual state
            actual = frontier.pop()  # LIFO
            self.explored_states += 1

            # Check depth limit
            parent = discovered[actual]
            depth = depths[parent] + 1 if parent else 0
            if depth <= self.max_depth:
                depths[actual] = depth

                # Verify if goal is reached
                if actual == self.env.goal_pos:
                    return self._parse_path(discovered)
                else:
                    borders = self._get_borders(actual, discovered)
                    for border in borders:
                        frontier.push(border)
                        discovered[border] = actual

        # Return failure -> empty path
        return []


class GoalAgentUCS(GoalBasedAgent2D):
    # Weights fixed at 1, so like BFS
    def __init__(self, env: Environment):
        super(GoalAgentUCS, self).__init__(env)

    def think(self) -> list:
        # Init queue and discovered dict (hashed)
        frontier = PriorityQueue()
        frontier.push(0, self.env.init_pos)
        discovered = {self.env.init_pos: None}  # And save parents

        # UCS main
        while len(frontier) > 0:
            # Prepare actual state
            actual_weight, actual = frontier.pop()  # FIFO with priority
            self.explored_states += 1

            # Verify if goal is reached
            if actual == self.env.goal_pos:
                return self._parse_path(discovered)
            else:
                borders = self._get_borders(actual, discovered)
                for border in borders:
                    frontier.push(actual_weight + 1, border)
                    discovered[border] = actual

        # Return failure -> empty path
        return []


if __name__ == '__main__':
    # Print grid and show agent's behavior.
    env = Environment((10, 10),
                      (random.randint(0, 10 - 1), random.randint(0, 10 - 1)),
                      (random.randint(0, 10 - 1), random.randint(0, 10 - 1)),
                      0.075)

    print(env)

    for agent_type in [GoalAgentBFS, GoalAgentDFS, GoalAgentDLS, GoalAgentUCS]:
        if agent_type == GoalAgentDLS:
            agent = agent_type(env, 3)
        else:
            agent = agent_type(env)

        path = agent.think()

        print(f'{agent_type.__name__}, solution_length={len(path)}, explored_states={agent.explored_states}, {path=}')
