"""
Unit tests for the CLI class in the labmateai module.
"""

import unittest
from unittest.mock import patch
from labmateai.cli import CLI
from labmateai.data_loader import load_tools_from_json


class TestCLI(unittest.TestCase):
    """
    Unit tests for the CLI class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the CLI instance before all tests.
        """
        cls.tools = load_tools_from_json('tools.json')
        cls.cli = CLI(cls.tools)

    @patch('builtins.input', side_effect=['1', 'Seurat', '3', '4'])
    def test_tool_recommendation(self, mock_input):
        """
        Test recommending tools similar to a specific tool.
        """
        with patch('builtins.print') as mock_print:
            self.cli.start()
            # Collect all printed outputs
            printed_texts = [call_args[0][0]
                             for call_args in mock_print.call_args_list]
            # Ensure that recommendations are printed
            self.assertTrue(any('Seurat' in text for text in printed_texts))
            self.assertTrue(any('recommendations' in text.lower()
                            for text in printed_texts))

    @patch('builtins.input', side_effect=['2', 'Genomics', '4'])
    def test_category_recommendation(self, mock_input):
        """
        Test recommending tools from a category.
        """
        with patch('builtins.print') as mock_print:
            self.cli.start()
            printed_texts = [call_args[0][0]
                             for call_args in mock_print.call_args_list]
            # Check that tools in the 'Genomics' category are listed
            self.assertTrue(any('Genomics' in text for text in printed_texts))

    @patch('builtins.input', side_effect=['3', 'RNA', '4'])
    def test_search_by_keyword(self, mock_input):
        """
        Test searching tools by a keyword.
        """
        with patch('builtins.print') as mock_print:
            self.cli.start()
            printed_texts = [call_args[0][0]
                             for call_args in mock_print.call_args_list]
            # Ensure that tools related to 'RNA' are displayed
            self.assertTrue(any('RNA' in text for text in printed_texts))
