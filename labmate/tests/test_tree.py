"""
Unit tests for the ToolTree class and its methods.
"""

import unittest
from labmate.tree import ToolTree, TreeNode
from labmate.data_loader import load_tools_from_json


class TestToolTree(unittest.TestCase):
    """
    Unit tests for the ToolTree and TreeNode classes.
    """

    @classmethod
    def setUpClass(cls):
        """
        Load tools and set up the ToolTree instance before all tests.
        """
        cls.tools = load_tools_from_json('data/tools.json')
        cls.tree = ToolTree()
        cls.tree.build_tree(cls.tools)

    def test_add_tool(self):
        """
        Test adding a tool to the tree.
        """
        new_tool = TreeNode(
            'NewTool', tool={'name': 'NewTool', 'category': 'Bioinformatics'})
        self.tree.add_tool(new_tool)
        category_node = self.tree.find_category_node('Bioinformatics')
        self.assertTrue(
            any(child.name == 'NewTool' for child in category_node.children))

    def test_get_tools_in_category(self):
        """
        Test getting all tools within a specific category.
        """
        tools_in_genomics = self.tree.get_tools_in_category('Genomics')
        self.assertGreater(len(tools_in_genomics), 0)
        self.assertTrue(
            any(tool.category == 'Genomics' for tool in tools_in_genomics))

    def test_search_tools(self):
        """
        Test searching for tools using a keyword.
        """
        results = self.tree.search_tools('Quality')
        self.assertGreater(len(results), 0)
        self.assertTrue(any('Quality' in tool.description for tool in results))
