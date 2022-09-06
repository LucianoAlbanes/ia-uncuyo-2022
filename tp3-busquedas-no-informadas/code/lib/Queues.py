from collections import deque


class PriorityQueue:
    # Placeholder, poor implemented. See heap-tree
    # Return min value
    __slots__ = 'list'

    def __init__(self):
        self.list = []

    def push(self, priority: int, value):
        self.list.append((priority, value))

    def pop(self):
        self.list.sort(key=lambda t: t[0])
        return self.list.pop()

    def __len__(self):
        return self.list.__len__()


class Queue:
    __slots__ = 'list'

    def __init__(self):
        self.list = deque()

    def push(self, value):
        self.list.append(value)

    def pop(self):
        return self.list.pop()

    def __len__(self):
        return self.list.__len__()


class Stack:
    __slots__ = 'list'

    def __init__(self):
        self.list = deque()

    def push(self, value):
        self.list.append(value)

    def pop(self):
        return self.list.popleft()

    def __len__(self):
        return self.list.__len__()