"""
This module provides a class to manage a queue of recommendation requests.
"""

from collections import deque


class RequestQueue:
    """
    A class to manage a queue of recommendation requests.
    """

    def __init__(self):
        """
        Initializes the RequestQueue an empty request queue.
        """
        self.queue = deque()

    def add_request(self, request):
        """
        Adds a request to the queue.

        Args:
            request: The request to be added to the queue.
        """

        self.queue.append(request)

    def process_next(self):
        """
        Processes the next request in the queue.

        Returns:
            The next request if available, None otherwise.
        """

        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        """
        Checks if the request queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """

        return len(self.queue) == 0

    def clear(self):
        """
        Clears all requests from the queue.
        """

        self.queue.clear()
