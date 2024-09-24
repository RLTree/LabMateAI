"""
Unit tests for the ToolTree class and its methods.
"""

import unittest
from labmateai.tree import ToolTree
from labmateai.data_loader import load_tools_from_json


class TestToolTree(unittest.TestCase):
    """
    Unit tests for the ToolTree class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the ToolTree instance before all tests.
        """
        cls.tools = load_tools_from_json('tools.json')
        cls.tree = ToolTree()
        cls.tree.build_tree(cls.tools)

    def test_get_tools_in_category(self):
        """
        Test retrieving tools in a category.
        """
        tools = self.tree.get_tools_in_category('Genomics')
        self.assertGreater(len(tools), 0)
        for tool in tools:
            self.assertEqual(tool.category, 'Genomics')

    def test_search_tools(self):
        """
        Test searching for tools by keyword.
        """
        results = self.tree.search_tools('Analysis')
        self.assertGreater(len(results), 0)
        self.assertTrue(
            any('Analysis' in tool.description for tool in results))

    def test_get_all_categories(self):
        """
        Test retrieving all categories.
        """
        categories = self.tree.get_all_categories()
        self.assertIn('Genomics', categories)
        self.assertIn('Bioinformatics', categories)
