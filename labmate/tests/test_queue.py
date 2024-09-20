"""
Unit tests for the RequestQueue class.
"""

import unittest
from labmate.queue import RequestQueue


class TestRequestQueue(unittest.TestCase):
    """
    Unit tests for the RequestQueue class.
    """

    def setUp(self):
        """
        Set up a new instance of RequestQueue before each test.
        """
        self.queue = RequestQueue()

    def test_add_request(self):
        """
        Test adding requests to the queue.
        """
        request = {'tool_name': 'FastQC', 'type': 'similar'}
        self.queue.add_request(request)
        self.assertEqual(len(self.queue.queue), 1)
        self.assertEqual(self.queue.queue[0], request)

    def test_process_next(self):
        """
        Test processing the next request in the queue.
        """
        request1 = {'tool_name': 'FastQC', 'type': 'similar'}
        request2 = {'category_name': 'Genomics', 'type': 'category'}
        self.queue.add_request(request1)
        self.queue.add_request(request2)

        next_request = self.queue.process_next()
        self.assertEqual(next_request, request1)
        self.assertEqual(len(self.queue.queue), 1)

    def test_is_empty(self):
        """
        Test if the queue correctly identifies when it is empty.
        """
        self.assertTrue(self.queue.is_empty())
        request = {'tool_name': 'BLAST', 'type': 'similar'}
        self.queue.add_request(request)
        self.assertFalse(self.queue.is_empty())

    def test_clear_queue(self):
        """
        Test clearing the queue.
        """
        request = {'tool_name': 'HISAT2', 'type': 'similar'}
        self.queue.add_request(request)
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())
