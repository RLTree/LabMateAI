# labmateai/tests/test_recommender_interface.py

"""
Test Suite for RecommenderInterface Module in LabMateAI.

This test suite ensures that the RecommenderInterface abstract base class is correctly defined
and that any concrete subclasses adhere to its contract.
"""

import unittest
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from labmateai.recommenders.recommender_interface import RecommenderInterface


class MockRecommender(RecommenderInterface):
    """
    A mock recommender class that correctly implements all abstract methods.
    Used for testing purposes.
    """

    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        return []

    def get_recommendation_scores(self, identifier: str) -> Dict[int, float]:
        return {}

    def display_recommendations(self, recommendations: List[Dict]) -> None:
        pass


class IncompleteRecommender(RecommenderInterface):
    """
    A mock recommender class that does NOT implement all abstract methods.
    Used to test enforcement of method implementation.
    """

    def recommend(
        self,
        user_id: Optional[int] = None,
        tool_name: Optional[str] = None,
        num_recommendations: int = 5
    ) -> List[Dict]:
        return []


class TestRecommenderInterface(unittest.TestCase):
    """
    Test cases for the RecommenderInterface abstract base class.
    """

    def test_cannot_instantiate_interface(self):
        """
        Test that instantiating RecommenderInterface directly raises a TypeError.
        """
        with self.assertRaises(TypeError):
            RecommenderInterface()

    def test_can_instantiate_concrete_recommender(self):
        """
        Test that a concrete recommender implementing all abstract methods can be instantiated.
        """
        try:
            mock_recommender = MockRecommender()
        except TypeError:
            self.fail("MockRecommender should implement all abstract methods and be instantiable.")
        self.assertIsInstance(mock_recommender, RecommenderInterface)

    def test_cannot_instantiate_incomplete_recommender(self):
        """
        Test that instantiating a subclass that doesn't implement all abstract methods raises a TypeError.
        """
        with self.assertRaises(TypeError):
            IncompleteRecommender()

    def test_concrete_recommender_methods(self):
        """
        Test that the concrete recommender's methods behave as expected.
        This is a basic test to ensure that the implemented methods can be called without errors.
        """
        mock_recommender = MockRecommender()
        try:
            recommendations = mock_recommender.recommend(user_id=1, tool_name="Alpha", num_recommendations=3)
            scores = mock_recommender.get_recommendation_scores(identifier="Alpha")
            mock_recommender.display_recommendations(recommendations)
        except Exception as e:
            self.fail(f"Methods in MockRecommender raised an exception unexpectedly: {e}")
        self.assertIsInstance(recommendations, list)
        self.assertIsInstance(scores, dict)

    def test_repr_method(self):
        """
        Test the __repr__ method of the RecommenderInterface.
        """
        mock_recommender = MockRecommender()
        expected_repr = "MockRecommender()"
        self.assertEqual(repr(mock_recommender), expected_repr)


class TestRecommenderInterfaceCompliance(unittest.TestCase):
    """
    Test cases to ensure that any subclass of RecommenderInterface complies with its method signatures.
    """

    def test_recommender_interface_method_signatures(self):
        """
        Test that concrete recommender classes implement methods with correct signatures.
        """
        mock_recommender = MockRecommender()

        # Test 'recommend' method signature
        recommend_method = mock_recommender.recommend
        self.assertEqual(recommend_method.__code__.co_argcount, 4)  # self, user_id, tool_name, num_recommendations

        # Test 'get_recommendation_scores' method signature
        get_scores_method = mock_recommender.get_recommendation_scores
        self.assertEqual(get_scores_method.__code__.co_argcount, 2)  # self, identifier

        # Test 'display_recommendations' method signature
        display_method = mock_recommender.display_recommendations
        self.assertEqual(display_method.__code__.co_argcount, 2)  # self, recommendations

    def test_recommender_interface_method_types(self):
        """
        Test that the methods return the expected types.
        """
        mock_recommender = MockRecommender()

        # 'recommend' should return List[Dict]
        recommendations = mock_recommender.recommend(user_id=1, tool_name="Alpha", num_recommendations=2)
        self.assertIsInstance(recommendations, list)
        for item in recommendations:
            self.assertIsInstance(item, dict)

        # 'get_recommendation_scores' should return Dict[int, float]
        scores = mock_recommender.get_recommendation_scores(identifier="Alpha")
        self.assertIsInstance(scores, dict)
        for key, value in scores.items():
            self.assertIsInstance(key, int)
            self.assertIsInstance(value, float)

        # 'display_recommendations' should return None
        result = mock_recommender.display_recommendations(recommendations)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
