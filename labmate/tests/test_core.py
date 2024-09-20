"""
Unit tests for the LabMateCore class.
"""

import unittest
from unittest.mock import patch
from labmate.core import LabMateCore
from labmate.data_loader import load_tools_from_json


class TestLabMateCore(unittest.TestCase):
    """
    Unit tests for the LabMateCore class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the LabMateCore instance before all tests.
        """
        cls.tools = load_tools_from_json('data/tools.json')
        cls.core = LabMateCore(cls.tools)

    def test_add_request_to_queue(self):
        """
        Test adding a request to the queue.
        """
        request = {'tool_name': 'BLAST', 'type': 'similar'}
        self.core.add_request_to_queue(request)
        self.assertEqual(len(self.core.request_queue), 1)

    def test_process_queue(self):
        """
        Test processing requests in the queue.
        """
        request1 = {'tool_name': 'FastQC', 'type': 'similar'}
        request2 = {'category_name': 'Genomics', 'type': 'category'}
        self.core.add_request_to_queue(request1)
        self.core.add_request_to_queue(request2)

        with patch('builtins.print') as mock_print:
            self.core.process_queue()
            # Ensure results were printed for both requests
            self.assertEqual(mock_print.call_count, 2)
