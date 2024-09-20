"""
Unit tests for the Recommender class.
"""

import unittest
from labmate.recommender import Recommender
from labmate.data_loader import load_tools_from_json


class TestRecommender(unittest.TestCase):
    """
    Unit tests for the Recommender class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Load tools and set up the Recommender instance before all tests.
        """
        cls.tools = load_tools_from_json('data/tools.json')
        cls.recommender = Recommender(cls.tools)

    def test_recommend_similar_tools(self):
        """
        Test recommending similar tools to a given tool.
        """
        recommendations = self.recommender.recommend_similar_tools(
            'FastQC', num_recommendations=3)
        self.assertEqual(len(recommendations), 3)
        self.assertTrue(any(tool.name == 'BLAST' for tool in recommendations))

    def test_recommend_tools_in_category(self):
        """
        Test recommending tools in a specific category.
        """
        recommendations = self.recommender.recommend_tools_in_category(
            'Genomics')
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(
            any(tool.category == 'Genomics' for tool in recommendations))

    def test_search_and_recommend(self):
        """
        Test searching for tools using a keyword.
        """
        recommendations = self.recommender.search_and_recommend('RNA')
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(
            any('RNA' in tool.description for tool in recommendations))
