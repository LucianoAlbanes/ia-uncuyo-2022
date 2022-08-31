import random

# Def Classes


class Environment:
    __slots__ = ('size_x', 'size_y', 'init_pos_x', 'init_pos_y', 'grid', 'dirt_rate', 'initial_dirt', 'cleaned_slots')

    def __init__(self, size_x: int, size_y: int, init_pos_x: int, init_pos_y: int, dirt_rate: float):
        # Size
        if size_x <= 0 or size_y <= 0:
            raise Exception('Size must be greater than 0.')
        self.size_x = size_x
        self.size_y = size_y

        # Init pos
        if init_pos_x >= size_x or init_pos_y >= size_y:
            raise Exception('Illegal initial position.')
        self.init_pos_x = init_pos_x
        self.init_pos_y = init_pos_y

        # Dirt
        if dirt_rate < 0 or dirt_rate > 1:
            raise Exception('Dirt rate must be between 0 and 1.')
        self.dirt_rate = dirt_rate

        # Proceed to initialize the grid
        self.initial_dirt = 0
        self.cleaned_slots = 0
        self._initialize_grid()

    def _initialize_grid(self):
        def _dirt() -> bool:
            dirty = random.random() < self.dirt_rate
            if dirty:
                self.initial_dirt += 1
            return dirty

        # Generate matrix
        self.grid = [[_dirt() for _ in range(self.size_x)] for _ in range(self.size_y)]

    def is_valid_movement(self, pos_x, pos_y, direction: str):
        match direction:
            case 'up':
                return pos_y - 1 >= 0
            case 'down':
                return pos_y + 1 < self.size_y
            case 'left':
                return pos_x - 1 >= 0
            case 'right':
                return pos_x + 1 < self.size_y
            case _:
                raise Exception('Invalid argument')

    def is_dirty(self, pos_x, pos_y):
        return self.grid[pos_x][pos_y]

    def get_performance(self):
        return {
            'initial_dirt': self.initial_dirt,
            'cleaned_slots': self.cleaned_slots
        }

    def print_environment(self):
        def _colorize(x):
            if x:
                return '💩'
            else:
                return ' '

        for m in self.grid:
            print([_colorize(x) for x in m])
        pass

    def clean(self, pos_x, pos_y) -> bool:
        # Returns the previous state of the slot
        dirty = self.is_dirty(pos_x, pos_y)
        if dirty:
            self.cleaned_slots += 1
        self.grid[pos_x][pos_y] = False
        return dirty


class InvalidMovementException(Exception):
    def __init__(self, direction: str):
        super(InvalidMovementException, self).__init__(f'Invalid movement. ${direction}')


class Agent:
    __slots__ = ('env', 'pos_x', 'pos_y')

    def __init__(self, env: Environment):
        self.env = env
        self.pos_x = env.init_pos_x
        self.pos_y = env.init_pos_y

    def up(self):
        if self.env.is_valid_movement(self.pos_x, self.pos_y, 'up'):
            self.pos_y -= 1
        else:
            raise InvalidMovementException('up')

    def down(self):
        if self.env.is_valid_movement(self.pos_x, self.pos_y, 'down'):
            self.pos_y += 1
        else:
            raise InvalidMovementException('down')

    def left(self):
        if self.env.is_valid_movement(self.pos_x, self.pos_y, 'left'):
            self.pos_x -= 1
        else:
            raise InvalidMovementException('left')

    def right(self):
        if self.env.is_valid_movement(self.pos_x, self.pos_y, 'right'):
            self.pos_x += 1
        else:
            raise InvalidMovementException('right')

    def suck(self):
        self.env.clean(self.pos_x, self.pos_y)

    def idle(self):
        pass

    def perspective(self):
        pass

    def think(self):
        pass


class SimpleReflexAgent(Agent):
    def __init__(self, env: Environment):
        super(SimpleReflexAgent, self).__init__(env)

    def perspective(self):
        # Checks if the current slot is dirty
        return self.env.is_dirty(self.pos_x, self.pos_y)

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
            dir_index = random.randint(0, len(directions)-1)

            # Try to move, else catch exception and increment
            while not moved:
                try:
                    getattr(self, directions[dir_index])()
                    moved = True
                except InvalidMovementException:
                    dir_index = (dir_index + 1) % len(directions)


class DumbAgent(Agent):
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
