"""
Unit tests for the Recommender class.
"""

import unittest
from labmateai.recommender import Recommender
from labmateai.data_loader import load_tools_from_json


class TestRecommender(unittest.TestCase):
    """
    Unit tests for the Recommender class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Load tools and set up the Recommender instance before all tests.
        """
        cls.tools = load_tools_from_json('tools.json')
        cls.recommender = Recommender(cls.tools)

    def test_recommend_similar_tools(self):
        """
        Test recommending similar tools.
        """
        recommendations = self.recommender.recommend_similar_tools('Seurat', 3)
        self.assertEqual(len(recommendations), 3)
        self.assertNotIn('Seurat', [tool.name for tool in recommendations])

    def test_recommend_tools_in_category(self):
        """
        Test recommending tools from a category.
        """
        recommendations = self.recommender.recommend_tools_in_category(
            'Genomics')
        self.assertGreater(len(recommendations), 0)
        for tool in recommendations:
            self.assertEqual(tool.category, 'Genomics')

    def test_search_and_recommend(self):
        """
        Test searching tools by keyword.
        """
        recommendations = self.recommender.search_and_recommend('RNA')
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(
            any('RNA' in tool.name or 'RNA' in tool.description for tool in recommendations))

    def test_invalid_tool_name(self):
        """
        Test handling of invalid tool names.
        """
        with self.assertRaises(ValueError):
            self.recommender.recommend_similar_tools('NonExistentTool', 3)
