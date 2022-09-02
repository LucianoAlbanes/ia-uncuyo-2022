import random


# Def Classes


def access_matrix(matrix: list, vector: list):
    prev = matrix
    for i in vector:
        prev = prev[i]
    return prev


def set_matrix(matrix: list, vector: list, value):
    prev = matrix
    for i in range(len(vector) - 1):
        prev = prev[vector[i]]
    prev[vector[-1]] = value


class Environment:
    # n-dimensional
    __slots__ = ('shape', 'init_pos', 'grid', 'dirt_rate', 'initial_dirt', 'cleaned_slots')

    def __init__(self, shape: list, init_pos: list, dirt_rate: float):
        # Size
        if min(shape) <= 0:
            raise Exception('All dimensions sizes must be positive.')
        self.shape = shape

        # Init pos (Verifies: 1. Same # of dimensions, 2. All init_pos must be positive 3. Valid init_pos in each dim.
        if len(shape) != len(init_pos) or min(init_pos) < 0 or False in [(a > b) for a, b in zip(shape, init_pos)]:
            raise Exception('Illegal initial position.')
        self.init_pos = init_pos

        # Dirt
        if dirt_rate < 0 or dirt_rate > 1:
            raise Exception('Dirt rate must be between 0 and 1.')
        self.dirt_rate = dirt_rate

        # Proceed to initialize the grid
        self.initial_dirt = 0
        self.cleaned_slots = 0
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        def _dirt() -> bool:
            dirty = random.random() < self.dirt_rate
            if dirty:
                self.initial_dirt += 1
            return dirty

        def _gen_dims(depth=1):
            if depth == len(self.shape):
                return [_dirt() for _ in range(self.shape[depth - 1])]
            else:
                return [_gen_dims(depth + 1) for _ in range(self.shape[depth - 1])]

        # Generate matrix
        self.grid = _gen_dims()

    def is_valid_movement(self, pos: list, direction: list):
        end_pos = [x + y for x, y in zip(pos, direction)]
        return min(end_pos) >= 0 and False not in [(a > b) for a, b in zip(self.shape, end_pos)]

    def is_dirty(self, pos: list):
        return access_matrix(self.grid, pos)

    def get_performance(self):
        return {
            'cleaned_slots': self.cleaned_slots
        }

    def __str__(self) -> str:
        # Only implemented for 1D and 2D grids
        def _colorize(x):
            if x:
                return 'x'
            else:
                return ' '

        txt = ''
        match len(self.shape):
            case 1:
                txt += str([_colorize(x) for x in self.grid]) + '\n'
            case 2:
                row: list   # Var hint
                for row in self.grid:
                    txt += str(([_colorize(x) for x in row])) + '\n'
            case _:
                raise NotImplementedError('Method only available for 1D and 2D environments')

        return txt

    def clean(self, pos: list) -> bool:
        # Returns the previous state of the slot
        dirty = self.is_dirty(pos)
        if dirty:
            self.cleaned_slots += 1
        set_matrix(self.grid, pos, False)
        return dirty


class InvalidMovementException(Exception):
    def __init__(self, direction):
        super(InvalidMovementException, self).__init__(f'Invalid movement. ${direction}')


class Agent2D:
    __slots__ = ('env', 'pos')

    def __init__(self, env: Environment):
        self.env = env
        self.pos = env.init_pos

    def up(self):
        if self.env.is_valid_movement(self.pos, [-1, 0]):
            self.pos[0] -= 1
        else:
            raise InvalidMovementException('up')

    def down(self):
        if self.env.is_valid_movement(self.pos, [1, 0]):
            self.pos[0] += 1
        else:
            raise InvalidMovementException('down')

    def left(self):
        if self.env.is_valid_movement(self.pos, [0, -1]):
            self.pos[1] -= 1
        else:
            raise InvalidMovementException('left')

    def right(self):
        if self.env.is_valid_movement(self.pos, [0, 1]):
            self.pos[1] += 1
        else:
            raise InvalidMovementException('right')

    def suck(self):
        self.env.clean(self.pos)

    def idle(self):
        pass

    def perspective(self):
        pass

    def think(self):
        pass


class SimpleReflexAgent(Agent2D):
    def __init__(self, env: Environment):
        super(SimpleReflexAgent, self).__init__(env)

    def perspective(self):
        # Checks if the current slot is dirty
        return self.env.is_dirty(self.pos)

    def think(self):
        # This agent only perspective is if the slot where its located is dirty or not.
        # If is dirty, it proceeds to clean it.
        if self.perspective():
            self.suck()

        # Else, will move randomly to any possible direction
        else:
            # Find next move randomly
            moved = False
            directions = ['up', 'down', 'left', 'right']
            dir_index = random.randint(0, len(directions) - 1)

            # Try to move, else catch exception and increment
            while not moved:
                try:
                    getattr(self, directions[dir_index])()
                    moved = True
                except InvalidMovementException:
                    dir_index = (dir_index + 1) % len(directions)


class DumbAgent(Agent2D):
    def __init__(self, env: Environment):
        super(DumbAgent, self).__init__(env)

    def think(self):
        # Try to perform any action
        acted = False
        actions = ['up', 'down', 'left', 'right', 'suck']
        act_index = random.randint(0, len(actions) - 1)

        # Try to perform action, if was a movement, increment index
        while not acted:
            try:
                getattr(self, actions[act_index])()
                acted = True
            except InvalidMovementException:
                act_index = (act_index + 1) % len(actions)
