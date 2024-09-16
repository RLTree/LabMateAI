"""
This module implements a basic Queue data structure.

A Queue is a collection of elements that supports two main operations:
- Enqueue: Adds an element to the end of the queue.
- Dequeue: Removes an element from the front of the queue.

The Queue follows (FIFO) principle. The first element added is the first one to be removed.
"""


class Queue:
    """
    A class to represent a queue data structure.

    Attributes
    ----------
    items : list
        A list to store the elements of the queue.
    """

    def __init__(self):
        """
        Initializes an empty queue.
        """
        self.items = []

    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.

        Args:
            item: The item to be added to the queue.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the item from the front of the queue.

        Returns:
            The item at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self.items.pop(0)

    def size(self):
        """
        Returns the number of items in the queue.

        Returns:
            int: The number of items in the queue.
        """
        return len(self.items)

    def peek(self):
        """
        Returns the item at the front of the queue without removing it.

        Returns:
            The item at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self.items[0]

    def clear(self):
        """
        Removes all items from the queue.
        """
        self.items = []
