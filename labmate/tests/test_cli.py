"""
Unit tests for the CLI class in the labmate module.
"""

import unittest
from unittest.mock import patch
from labmate.cli import CLI
from labmate.data_loader import load_tools_from_json


class TestCLI(unittest.TestCase):
    """
    Unit tests for the CLI class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the CLI instance before all tests.
        """
        cls.tools = load_tools_from_json('data/tools.json')
        cls.cli = CLI(cls.tools)

    @patch('builtins.input', side_effect=['--tool FastQC', '--num 3'])
    def test_tool_recommendation(self):
        """
        Test recommending tools via CLI input for similar tools.
        """
        with patch('builtins.print') as mock_print:
            self.cli.start()
            mock_print.assert_called()  # Ensure something was printed
            self.assertIn('FastQC', mock_print.call_args[0][0])

    @patch('builtins.input', side_effect=['--category Genomics'])
    def test_category_recommendation(self):
        """
        Test recommending tools via CLI input for a category.
        """
        with patch('builtins.print') as mock_print:
            self.cli.start()
            mock_print.assert_called()
            self.assertIn('Genomics', mock_print.call_args[0][0])
