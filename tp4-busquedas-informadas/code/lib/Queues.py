from heapq import heappop, heappush


class PriorityQueue:
    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    __slots__ = ('list', 'count')

    def __init__(self):
        self.list = []
        self.count = 0

    def push(self, priority: int, value):
        self.count += 1
        return heappush(self.list, (priority, self.count, value))

    def pop(self):
        v = heappop(self.list)  # Remove counter
        return v[0], v[2]

    def __len__(self):
        return self.list.__len__()


class Queue:  # FIFO
    __slots__ = 'list'

    def __init__(self):
        self.list = []

    def push(self, value):
        self.list.append(value)

    def pop(self):
        return self.list.pop(0)

    def __len__(self):
        return self.list.__len__()


class Stack:  # LIFO
    __slots__ = 'list'

    def __init__(self):
        self.list = []

    def push(self, value):
        self.list.append(value)

    def pop(self):
        return self.list.pop()

    def __len__(self):
        return self.list.__len__()
