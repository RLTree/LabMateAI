# labmateai/tests/test_hybrid_recommender.py

"""
Test Suite for HybridRecommender Module in LabMateAI.

This test suite ensures that the HybridRecommender class correctly implements the RecommenderInterface
and functions as expected when combining content-based and collaborative filtering.
"""

import unittest
import pandas as pd
from unittest.mock import MagicMock, patch
from labmateai.recommenders.hybrid_recommender import HybridRecommender
from labmateai.recommenders.recommender_interface import RecommenderInterface
from labmateai.recommenders.collaborative_recommender import CollaborativeRecommender
from labmateai.recommenders.content_based_recommender import ContentBasedRecommender


class TestHybridRecommender(unittest.TestCase):
    """
    Test cases for the HybridRecommender class.
    """

    def setUp(self):
        """
        Set up the HybridRecommender instance with mocked content and collaborative recommenders.
        This setup runs before each test to ensure test isolation.
        """
        # Mock ContentBasedRecommender
        self.mock_content_recommender = MagicMock(spec=ContentBasedRecommender)
        # Mock CollaborativeRecommender
        self.mock_collaborative_recommender = MagicMock(spec=CollaborativeRecommender)

        # Sample tools DataFrame for collaborative recommender
        self.collaborative_tools_data = {
            'tool_id': [1, 2, 3, 4],
            'name': ["Alpha", "Beta", "Gamma", "Delta"],
            'category': ["Genomics", "Proteomics", "Genomics", "Metabolomics"],
            'features': ["sequence_analysis;alignment",
                         "mass_spectrometry;protein_identification",
                         "variant_calling;genome_assembly",
                         "metabolite_profiling;pathway_analysis"],
            'cost': ["Free", "Paid", "Free", "Free"],
            'description': ["Alpha Description", "Beta Description", "Gamma Description", "Delta Description"],
            'url': ["http://alpha.com", "http://beta.com", "http://gamma.com", "http://delta.com"],
            'language': ["Python", "R", "Java", "Python"],
            'platform': ["Linux", "Windows", "Mac", "Linux"]
        }
        self.collaborative_tools_df = pd.DataFrame(self.collaborative_tools_data)
        self.mock_collaborative_recommender.tools_df = self.collaborative_tools_df

        # Sample tools DataFrame for content recommender
        self.content_tools_data = {
            'tool_id': [1, 2, 3, 4],
            'name': ["Alpha", "Beta", "Gamma", "Delta"],
            'category': ["Genomics", "Proteomics", "Genomics", "Metabolomics"],
            'features': ["sequence_analysis;alignment",
                         "mass_spectrometry;protein_identification",
                         "variant_calling;genome_assembly",
                         "metabolite_profiling;pathway_analysis"],
            'cost': ["Free", "Paid", "Free", "Free"],
            'description': ["Alpha Description", "Beta Description", "Gamma Description", "Delta Description"],
            'url': ["http://alpha.com", "http://beta.com", "http://gamma.com", "http://delta.com"],
            'language': ["Python", "R", "Java", "Python"],
            'platform': ["Linux", "Windows", "Mac", "Linux"]
        }
        self.content_tools_df = pd.DataFrame(self.content_tools_data)
        self.mock_content_recommender.tools_df = self.content_tools_df

        # Initialize HybridRecommender with alpha=0.6
        self.hybrid_recommender = HybridRecommender(
            content_recommender=self.mock_content_recommender,
            collaborative_recommender=self.mock_collaborative_recommender,
            alpha=0.6
        )

    def test_initialization_valid_alpha(self):
        """
        Test that HybridRecommender initializes correctly with a valid alpha.
        """
        self.assertEqual(self.hybrid_recommender.alpha, 0.6)
        self.assertEqual(self.hybrid_recommender.content_recommender, self.mock_content_recommender)
        self.assertEqual(self.hybrid_recommender.collaborative_recommender, self.mock_collaborative_recommender)

    def test_initialization_invalid_alpha_low(self):
        """
        Test that initializing HybridRecommender with alpha < 0 raises ValueError.
        """
        with self.assertRaises(ValueError) as context:
            HybridRecommender(
                content_recommender=self.mock_content_recommender,
                collaborative_recommender=self.mock_collaborative_recommender,
                alpha=-0.1
            )
        self.assertIn("Alpha must be between 0 and 1.", str(context.exception))

    def test_initialization_invalid_alpha_high(self):
        """
        Test that initializing HybridRecommender with alpha > 1 raises ValueError.
        """
        with self.assertRaises(ValueError) as context:
            HybridRecommender(
                content_recommender=self.mock_content_recommender,
                collaborative_recommender=self.mock_collaborative_recommender,
                alpha=1.5
            )
        self.assertIn("Alpha must be between 0 and 1.", str(context.exception))

    def test_recommend_valid_user_with_tool_name(self):
        """
        Test that recommend method combines CF and CBF scores correctly when both user_id and tool_name are provided.
        """
        user_id = 1
        tool_name = "Alpha"
        num_recommendations = 2

        # Mock collaborative_scores
        collaborative_scores = pd.Series({
            1: 4.5,
            2: 3.2,
            3: 4.8,
            4: 2.1
        })
        self.mock_collaborative_recommender.get_recommendation_scores.return_value = collaborative_scores

        # Mock content_scores
        content_scores = pd.Series({
            1: 0.0,  # Reference tool
            2: 0.6,
            3: 0.8,
            4: 0.2
        })
        self.mock_content_recommender.get_recommendation_scores.return_value = content_scores

        # Expected normalization
        expected_normalized_cf = (collaborative_scores - collaborative_scores.min()) / (collaborative_scores.max() - collaborative_scores.min())
        # (4.5-2.1)/(4.8-2.1) ≈ 0.6923
        # (3.2-2.1)/(4.8-2.1) ≈ 0.3333
        # (4.8-2.1)/(4.8-2.1) = 1.0
        # (2.1-2.1)/(4.8-2.1) = 0.0

        # Expected normalized_cb
        # (0.0-0.0)/(0.8-0.0) = 0.0
        # (0.6-0.0)/(0.8-0.0) = 0.75
        # (0.8-0.0)/(0.8-0.0) = 1.0
        # (0.2-0.0)/(0.8-0.0) = 0.25

        # Expected combined scores = 0.6 * normalized_cf + 0.4 * normalized_cb
        combined_scores = 0.6 * expected_normalized_cf + 0.4 * pd.Series({
            1: 0.0,
            2: 0.75,
            3: 1.0,
            4: 0.25
        })

        # Sorted: 3 (1.0), 2 (~0.49998)
        expected_top_tool_ids = [3, 2]

        # Mock the tools_df for retrieval
        self.mock_collaborative_recommender.tools_df = self.collaborative_tools_df

        # Call the recommend method
        recommendations = self.hybrid_recommender.recommend(
            user_id=user_id,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        # Assert that get_recommendation_scores was called correctly
        self.mock_collaborative_recommender.get_recommendation_scores.assert_called_once_with(user_id)
        self.mock_content_recommender.get_recommendation_scores.assert_called_once_with(tool_name)

        # Expected recommended tools
        expected_recommended_tools = self.collaborative_tools_df[self.collaborative_tools_df['tool_id'].isin(expected_top_tool_ids)].to_dict('records')

        # Assert that recommendations match expected
        self.assertEqual(recommendations, expected_recommended_tools)

    def test_recommend_valid_user_without_tool_name(self):
        """
        Test that recommend method generates recommendations based solely on collaborative filtering when tool_name is not provided.
        """
        user_id = 2
        tool_name = None
        num_recommendations = 3

        # Mock collaborative_scores
        collaborative_scores = pd.Series({
            1: 3.5,
            2: 4.0,
            3: 2.5,
            4: 4.5
        })
        self.mock_collaborative_recommender.get_recommendation_scores.return_value = collaborative_scores

        # Since tool_name is not provided, content_scores should NOT be called
        # Therefore, no need to set content_scores

        # Expected normalization
        expected_normalized_cf = (collaborative_scores - collaborative_scores.min()) / (collaborative_scores.max() - collaborative_scores.min())
        # (3.5-2.5)/(4.5-2.5) = 0.5
        # (4.0-2.5)/(4.5-2.5) = 0.75
        # (2.5-2.5)/(4.5-2.5) = 0.0
        # (4.5-2.5)/(4.5-2.5) = 1.0

        # Expected normalized_cb = 0 for all (since tool_name is None)
        # combined_scores = 0.6 * normalized_cf + 0.4 * 0 = 0.6 * normalized_cf

        # Sorted scores: 4 (0.6), 2 (0.45), 1 (0.3)
        expected_top_tool_ids = [4, 2, 1]

        # Mock the tools_df for retrieval
        self.mock_collaborative_recommender.tools_df = self.collaborative_tools_df

        # Call the recommend method
        recommendations = self.hybrid_recommender.recommend(
            user_id=user_id,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        # Assert that get_recommendation_scores was called correctly
        self.mock_collaborative_recommender.get_recommendation_scores.assert_called_once_with(user_id)
        self.mock_content_recommender.get_recommendation_scores.assert_not_called()

        # Expected recommended tools
        expected_recommended_tools = self.collaborative_tools_df[self.collaborative_tools_df['tool_id'].isin(expected_top_tool_ids)].to_dict('records')

        # Assert that recommendations match expected
        self.assertEqual(recommendations, expected_recommended_tools)

    def test_recommend_invalid_num_recommendations_low(self):
        """
        Test that recommend method raises ValueError when num_recommendations is less than 1.
        """
        user_id = 1
        tool_name = "Alpha"
        num_recommendations = 0

        with self.assertRaises(ValueError) as context:
            self.hybrid_recommender.recommend(
                user_id=user_id,
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        self.assertIn("num_recommendations must be at least 1.", str(context.exception))

    def test_recommend_neither_user_id_nor_tool_name_provided(self):
        """
        Test that recommend method raises ValueError when neither user_id nor tool_name is provided.
        """
        with self.assertRaises(ValueError) as context:
            self.hybrid_recommender.recommend(
                user_id=None,
                tool_name=None,
                num_recommendations=3
            )
        self.assertIn("At least one of user_id or tool_name must be provided for recommendations.", str(context.exception))

    def test_recommend_tool_not_found_in_content_recommender(self):
        """
        Test that recommend method raises ValueError when tool_name is not found in content recommender.
        """
        user_id = 1
        tool_name = "NonExistentTool"
        num_recommendations = 2

        # Mock collaborative_scores
        collaborative_scores = pd.Series({
            1: 4.5,
            2: 3.2,
            3: 4.8,
            4: 2.1
        })
        self.mock_collaborative_recommender.get_recommendation_scores.return_value = collaborative_scores

        # Mock content_scores to raise ValueError
        self.mock_content_recommender.get_recommendation_scores.side_effect = ValueError("Tool 'NonExistentTool' not found in the dataset.")

        with self.assertRaises(ValueError) as context:
            self.hybrid_recommender.recommend(
                user_id=user_id,
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        self.assertIn("Content-based filtering error: Tool 'NonExistentTool' not found in the dataset.", str(context.exception))
        self.mock_collaborative_recommender.get_recommendation_scores.assert_called_once_with(user_id)
        self.mock_content_recommender.get_recommendation_scores.assert_called_once_with(tool_name)

    def test_recommend_collaborative_recommender_error(self):
        """
        Test that recommend method raises ValueError when collaborative recommender raises an error.
        """
        user_id = 999  # Assume this user_id does not exist
        tool_name = "Alpha"
        num_recommendations = 2

        # Mock collaborative_scores to raise ValueError
        self.mock_collaborative_recommender.get_recommendation_scores.side_effect = ValueError("User ID 999 not found.")

        with self.assertRaises(ValueError) as context:
            self.hybrid_recommender.recommend(
                user_id=user_id,
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        self.assertIn("Collaborative filtering error: User ID 999 not found.", str(context.exception))
        self.mock_collaborative_recommender.get_recommendation_scores.assert_called_once_with(user_id)
        self.mock_content_recommender.get_recommendation_scores.assert_not_called()

    def test_recommend_no_collaborative_scores(self):
        """
        Test recommend method when user_id is not provided but tool_name is, ensuring content-based recommendations are used.
        """
        user_id = None
        tool_name = "Alpha"
        num_recommendations = 2

        # Mock collaborative_scores should NOT be called; hence, no need to set return_value

        # Mock content_scores
        content_scores = pd.Series({
            1: 0.0,  # Reference tool
            2: 0.6,
            3: 0.8,
            4: 0.2
        })
        self.mock_content_recommender.get_recommendation_scores.return_value = content_scores

        # Expected combined scores = 0.6 * 0 + 0.4 * content_scores = 0.4 * content_scores
        # Thus, scores: 1:0.0, 2:0.24, 3:0.32, 4:0.08

        # Sorted: 3 (0.32), 2 (0.24)
        expected_top_tool_ids = [3, 2]

        # Mock the tools_df for retrieval
        self.mock_collaborative_recommender.tools_df = self.collaborative_tools_df

        # Call the recommend method
        recommendations = self.hybrid_recommender.recommend(
            user_id=user_id,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        # Assert that get_recommendation_scores was called correctly
        self.mock_collaborative_recommender.get_recommendation_scores.assert_not_called()
        self.mock_content_recommender.get_recommendation_scores.assert_called_once_with(tool_name)

        # Expected recommended tools
        expected_recommended_tools = self.collaborative_tools_df[self.collaborative_tools_df['tool_id'].isin(expected_top_tool_ids)].to_dict('records')

        # Assert that recommendations match expected
        self.assertEqual(recommendations, expected_recommended_tools)

    def test_display_recommendations_with_results(self):
        """
        Test that display_recommendations method correctly prints the recommended tools.
        """
        recommendations = [
            {'tool_id': 1, 'name': "Alpha", 'category': "Genomics", 'language': "Python", 'platform': "Linux"},
            {'tool_id': 2, 'name': "Beta", 'category': "Proteomics", 'language': "R", 'platform': "Windows"}
        ]

        with patch('builtins.print') as mock_print:
            self.hybrid_recommender.display_recommendations(recommendations)
            mock_print.assert_any_call("Recommended Tools:")
            mock_print.assert_any_call("- Alpha (Category: Genomics, Language: Python, Platform: Linux)")
            mock_print.assert_any_call("- Beta (Category: Proteomics, Language: R, Platform: Windows)")

    def test_display_recommendations_no_results(self):
        """
        Test that display_recommendations method correctly handles empty recommendations.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.hybrid_recommender.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_get_recommendation_scores_with_user_id(self):
        """
        Test get_recommendation_scores method when identifier is a user_id.
        """
        identifier = "1"  # user_id as string
        collaborative_scores = pd.Series({
            1: 4.5,
            2: 3.2,
            3: 4.8,
            4: 2.1
        })
        self.mock_collaborative_recommender.get_recommendation_scores.return_value = collaborative_scores

        scores = self.hybrid_recommender.get_recommendation_scores(identifier)

        self.mock_collaborative_recommender.get_recommendation_scores.assert_called_once_with(1)
        self.mock_content_recommender.get_recommendation_scores.assert_not_called()

        expected_scores = collaborative_scores.to_dict()
        self.assertEqual(scores, expected_scores)

    def test_get_recommendation_scores_with_tool_name(self):
        """
        Test get_recommendation_scores method when identifier is a tool_name.
        """
        identifier = "Alpha"  # tool_name
        content_scores = pd.Series({
            1: 0.0,
            2: 0.6,
            3: 0.8,
            4: 0.2
        })
        self.mock_content_recommender.get_recommendation_scores.return_value = content_scores

        scores = self.hybrid_recommender.get_recommendation_scores(identifier)

        self.mock_collaborative_recommender.get_recommendation_scores.assert_not_called()
        self.mock_content_recommender.get_recommendation_scores.assert_called_once_with("Alpha")

        expected_scores = content_scores.to_dict()
        self.assertEqual(scores, expected_scores)

    def test_get_recommendation_scores_invalid_identifier(self):
        """
        Test get_recommendation_scores method when identifier is neither a valid user_id nor a valid tool_name.
        """
        identifier = "NonExistentIdentifier"

        # Mock content_recommender to raise ValueError
        self.mock_content_recommender.get_recommendation_scores.side_effect = ValueError("Identifier not found.")

        with self.assertRaises(ValueError) as context:
            self.hybrid_recommender.get_recommendation_scores(identifier)
        self.assertIn("Identifier not found.", str(context.exception))
        self.mock_collaborative_recommender.get_recommendation_scores.assert_not_called()
        self.mock_content_recommender.get_recommendation_scores.assert_called_once_with(identifier)

    def test_repr_method(self):
        """
        Test the __repr__ method for correct string representation.
        """
        expected_repr = (
            f"HybridRecommender(alpha=0.6, "
            f"content_recommender={repr(self.mock_content_recommender)}, "
            f"collaborative_recommender={repr(self.mock_collaborative_recommender)})"
        )
        self.assertEqual(repr(self.hybrid_recommender), expected_repr)


if __name__ == '__main__':
    unittest.main()
