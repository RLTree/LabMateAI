# labmateai/tests/test_collaborative_recommender.py

"""
Test Suite for CollaborativeRecommender Module in LabMateAI.

This test suite ensures that the CollaborativeRecommender class correctly implements the RecommenderInterface
and functions as expected when providing collaborative filtering-based recommendations.
"""

import unittest
from unittest.mock import MagicMock, patch
from labmateai.recommenders.collaborative_recommender import CollaborativeRecommender
from labmateai.recommenders.recommender_interface import RecommenderInterface
import pandas as pd
import numpy as np


class TestCollaborativeRecommender(unittest.TestCase):
    """
    Test cases for the CollaborativeRecommender class.
    """

    def setUp(self):
        """
        Set up the CollaborativeRecommender instance with mocked user-item matrix and tools_df.
        This setup runs before each test to ensure test isolation.
        """
        # Sample user-item interaction matrix
        self.user_item_data = {
            'tool_id': [1, 2, 3, 4],
            101: [5, 0, 3, 0],
            102: [4, 2, 0, 1],
            103: [0, 5, 4, 0],
            104: [0, 0, 5, 5],
            105: [1, 0, 0, 4]
        }
        self.user_item_matrix = pd.DataFrame(self.user_item_data).set_index('tool_id').T

        # Sample tools DataFrame
        self.tools_data = {
            'tool_id': [1, 2, 3, 4],
            'name': ["Alpha", "Beta", "Gamma", "Delta"],
            'category': ["Genomics", "Proteomics", "Genomics", "Metabolomics"],
            'features': ["sequence_analysis;alignment",
                         "mass_spectrometry;protein_identification",
                         "variant_calling;genome_assembly",
                         "metabolite_profiling;pathway_analysis"],
            'cost': [100, 200, 150, 120],
            'description': ["Alpha Description", "Beta Description", "Gamma Description", "Delta Description"],
            'url': ["http://alpha.com", "http://beta.com", "http://gamma.com", "http://delta.com"],
            'language': ["Python", "R", "Java", "Python"],
            'platform': ["Linux", "Windows", "Mac", "Linux"]
        }
        self.tools_df = pd.DataFrame(self.tools_data)

        # Initialize CollaborativeRecommender
        self.collab_recommender = CollaborativeRecommender(
            user_item_matrix=self.user_item_matrix,
            tools_df=self.tools_df,
            n_neighbors=2
        )

    def test_initialization_valid_inputs(self):
        """
        Test that CollaborativeRecommender initializes correctly with valid inputs.
        """
        self.assertEqual(self.collab_recommender.n_neighbors, 2)
        self.assertEqual(len(self.collab_recommender.all_tool_ids), 4)
        self.assertIn(1, self.collab_recommender.tool_id_to_details)
        self.assertIn(4, self.collab_recommender.tool_id_to_details)

    def test_initialization_empty_user_item_matrix(self):
        """
        Test that initializing CollaborativeRecommender with an empty user-item matrix raises ValueError.
        """
        empty_matrix = pd.DataFrame()
        with self.assertRaises(ValueError) as context:
            CollaborativeRecommender(
                user_item_matrix=empty_matrix,
                tools_df=self.tools_df
            )
        self.assertIn("User-item matrix is empty", str(context.exception))

    def test_initialization_missing_tool_ids(self):
        """
        Test that initializing CollaborativeRecommender with tool_ids not present in tools_df raises ValueError.
        """
        # Add a tool_id that is not in tools_df
        user_item_matrix = self.user_item_matrix.copy()
        user_item_matrix['5'] = [0, 1, 0, 2, 3]  # tool_id 5 not in tools_df

        with self.assertRaises(ValueError) as context:
            CollaborativeRecommender(
                user_item_matrix=user_item_matrix,
                tools_df=self.tools_df
            )
        # Relax the assertion to check if '5' is in the message
        self.assertIn("User-item matrix contains tool_ids not present in tools_df", str(context.exception))
        self.assertIn("5", str(context.exception))

    def test_initialization_duplicate_tool_ids(self):
        """
        Test that initializing CollaborativeRecommender with duplicate tool_ids in tools_df raises ValueError.
        """
        # Duplicate tool_id 1
        tools_df_dup = self.tools_df.copy()
        duplicate_tool = pd.DataFrame({
            'tool_id': [1],
            'name': ["Epsilon"],
            'category': ["Genomics"],
            'features': ["gene_expression"],
            'cost': [130],
            'description': ["Epsilon Description"],
            'url': ["http://epsilon.com"],
            'language': ["C++"],
            'platform': ["Linux"]
        })
        tools_df_dup = pd.concat([tools_df_dup, duplicate_tool], ignore_index=True)

        with self.assertRaises(ValueError) as context:
            CollaborativeRecommender(
                user_item_matrix=self.user_item_matrix,
                tools_df=tools_df_dup
            )
        self.assertIn("Duplicate tool_ids found in tools_df", str(context.exception))
        self.assertIn("1", str(context.exception))

    def test_initialization_invalid_n_neighbors(self):
        """
        Test that initializing CollaborativeRecommender with n_neighbors less than 1 raises ValueError.
        """
        with self.assertRaises(ValueError) as context:
            CollaborativeRecommender(
                user_item_matrix=self.user_item_matrix,
                tools_df=self.tools_df,
                n_neighbors=0
            )
        self.assertIn("n_neighbors must be at least 1.", str(context.exception))

    def test_recommend_valid_user(self):
        """
        Test that recommend method returns correct recommendations for a valid user.
        """
        user_id = 101
        num_recommendations = 2

        # Mock get_recommendation_scores to return predefined scores
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 4.5,
                2: 3.2,
                3: 4.8,
                4: 2.1
            }

            # Call recommend
            recommendations = self.collab_recommender.recommend(
                user_id=user_id,
                tool_name=None,
                num_recommendations=num_recommendations
            )

            # Verify get_recommendation_scores was called correctly
            mock_get_scores.assert_called_once_with(user_id)

            # Expected tool_ids: 2 and 4 (highest scores excluding already rated tools)
            # User 101 has rated tool_id 1 and 3 (ratings >0)
            expected_recommendations = [
                {
                    'tool_id': 2,
                    'tool_name': "Beta",
                    'category': "Proteomics",
                    'features': "mass_spectrometry;protein_identification",
                    'cost': 200,
                    'description': "Beta Description",
                    'url': "http://beta.com",
                    'language': "R",
                    'platform': "Windows"
                },
                {
                    'tool_id': 4,
                    'tool_name': "Delta",
                    'category': "Metabolomics",
                    'features': "metabolite_profiling;pathway_analysis",
                    'cost': 120,
                    'description': "Delta Description",
                    'url': "http://delta.com",
                    'language': "Python",
                    'platform': "Linux"
                }
            ]

            self.assertEqual(recommendations, expected_recommendations)

    def test_recommend_user_not_found(self):
        """
        Test that recommend method raises ValueError when user_id is not found in user_item_matrix.
        """
        user_id = 999  # Non-existent user_id
        num_recommendations = 2

        with self.assertRaises(ValueError) as context:
            self.collab_recommender.recommend(
                user_id=user_id,
                tool_name=None,
                num_recommendations=num_recommendations
            )
        self.assertIn(f"User ID {user_id} not found in the user-item matrix.", str(context.exception))

    def test_recommend_num_recommendations_less_than_one(self):
        """
        Test that recommend method raises ValueError when num_recommendations is less than 1.
        """
        user_id = 101
        num_recommendations = 0

        with self.assertRaises(ValueError) as context:
            self.collab_recommender.recommend(
                user_id=user_id,
                tool_name=None,
                num_recommendations=num_recommendations
            )
        self.assertIn("num_recommendations must be at least 1.", str(context.exception))

    def test_recommend_user_with_no_ratings(self):
        """
        Test that recommend method handles users with no ratings by returning top-rated tools.
        """
        user_id = 105  # Assuming user 105 has minimal or no ratings
        num_recommendations = 2

        # Mock get_recommendation_scores_by_user to return average ratings
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 2.5, # Already rated by user 105
                2: 3.5,
                3: 4.0,
                4: 4.5 # Alreay rated by user 105
            }

            # Call recommend
            recommendations = self.collab_recommender.recommend(
                user_id=user_id,
                tool_name=None,
                num_recommendations=num_recommendations
            )

            # Expected tool_ids: 4 and 3 (highest average scores)
            expected_recommendations = [
                {
                    'tool_id': 3,
                    'tool_name': "Gamma",
                    'category': "Genomics",
                    'features': "variant_calling;genome_assembly",
                    'cost': 150,
                    'description': "Gamma Description",
                    'url': "http://gamma.com",
                    'language': "Java",
                    'platform': "Mac"
                },
                {
                    'tool_id': 2,
                    'tool_name': "Beta",
                    'category': "Proteomics",
                    'features': "mass_spectrometry;protein_identification",
                    'cost': 200,
                    'description': "Beta Description",
                    'url': "http://beta.com",
                    'language': "R",
                    'platform': "Windows"
                }
            ]

            self.assertEqual(recommendations, expected_recommendations)

    def test_get_recommendation_scores_valid_user(self):
        """
        Test that get_recommendation_scores returns correct scores for a valid user.
        """
        user_id = 102

        # Mock get_recommendation_scores_by_user
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 4.0,
                2: 3.5,
                3: 4.5,
                4: 2.1
            }

            # Call get_recommendation_scores with user_id as string
            scores = self.collab_recommender.get_recommendation_scores("102")

            # Verify method was called correctly
            mock_get_scores.assert_called_once_with(user_id)

            expected_scores = {
                1: 4.0,
                2: 3.5,
                3: 4.5,
                4: 2.1
            }

            self.assertEqual(scores, expected_scores)

    def test_get_recommendation_scores_invalid_identifier(self):
        """
        Test that get_recommendation_scores raises ValueError when identifier is not a valid user ID.
        """
        identifier = "abc"  # Invalid user ID

        with self.assertRaises(ValueError) as context:
            self.collab_recommender.get_recommendation_scores(identifier)
        self.assertIn("Identifier must be a valid user ID represented as a string.", str(context.exception))

    def test_display_recommendations_with_results(self):
        """
        Test that display_recommendations method correctly prints the recommended tools.
        """
        recommendations = [
            {
                'tool_id': 2,
                'tool_name': "Beta",
                'category': "Proteomics",
                'features': "mass_spectrometry;protein_identification",
                'cost': 200,
                'description': "Beta Description",
                'url': "http://beta.com",
                'language': "R",
                'platform': "Windows"
            },
            {
                'tool_id': 4,
                'tool_name': "Delta",
                'category': "Metabolomics",
                'features': "metabolite_profiling;pathway_analysis",
                'cost': 120,
                'description': "Delta Description",
                'url': "http://delta.com",
                'language': "Python",
                'platform': "Linux"
            }
        ]

        with patch('builtins.print') as mock_print:
            self.collab_recommender.display_recommendations(recommendations)
            mock_print.assert_any_call("\nRecommended Tools:")
            mock_print.assert_any_call("- Beta - Beta Description (Category: Proteomics, Cost: $200)")
            mock_print.assert_any_call("- Delta - Delta Description (Category: Metabolomics, Cost: $120)")

    def test_display_recommendations_no_results(self):
        """
        Test that display_recommendations method correctly handles empty recommendations.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.collab_recommender.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_get_recommendation_scores_with_no_ratings(self):
        """
        Test that get_recommendation_scores returns average ratings when the user has no ratings.
        """
        user_id = 104  # Assume user 104 has no ratings

        # Mock get_recommendation_scores_by_user to return average ratings
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 2.5,
                2: 3.5,
                3: 4.0,
                4: 4.5
            }

            scores = self.collab_recommender.get_recommendation_scores("104")

            mock_get_scores.assert_called_once_with(user_id)

            expected_scores = {
                1: 2.5,
                2: 3.5,
                3: 4.0,
                4: 4.5
            }

            self.assertEqual(scores, expected_scores)

    def test_repr_method(self):
        """
        Test the __repr__ method for correct string representation.
        """
        expected_repr = "CollaborativeRecommender(n_neighbors=2, number_of_tools=4)"
        self.assertEqual(repr(self.collab_recommender), expected_repr)


class TestCollaborativeRecommenderInterfaceCompliance(unittest.TestCase):
    """
    Test cases to ensure that CollaborativeRecommender complies with RecommenderInterface.
    """

    def setUp(self):
        """
        Set up a mock CollaborativeRecommender instance.
        """
        # Sample user-item interaction matrix
        self.user_item_data = {
            'tool_id': [1, 2],
            101: [5, 0],
            102: [4, 2],
            103: [0, 5],
            104: [0, 0]
        }
        self.user_item_matrix = pd.DataFrame(self.user_item_data).set_index('tool_id').T

        # Sample tools DataFrame
        self.tools_data = {
            'tool_id': [1, 2],
            'name': ["Alpha", "Beta"],
            'category': ["Genomics", "Proteomics"],
            'features': ["sequence_analysis;alignment",
                         "mass_spectrometry;protein_identification"],
            'cost': [100, 200],
            'description': ["Alpha Description", "Beta Description"],
            'url': ["http://alpha.com", "http://beta.com"],
            'language': ["Python", "R"],
            'platform': ["Linux", "Windows"]
        }
        self.tools_df = pd.DataFrame(self.tools_data)

        # Initialize CollaborativeRecommender
        self.collab_recommender = CollaborativeRecommender(
            user_item_matrix=self.user_item_matrix,
            tools_df=self.tools_df,
            n_neighbors=1
        )

    def test_interface_methods_exist(self):
        """
        Test that CollaborativeRecommender implements all methods defined in RecommenderInterface.
        """
        self.assertTrue(hasattr(self.collab_recommender, 'recommend'))
        self.assertTrue(hasattr(self.collab_recommender, 'get_recommendation_scores'))
        self.assertTrue(hasattr(self.collab_recommender, 'display_recommendations'))
        self.assertTrue(hasattr(self.collab_recommender, '__repr__'))

    def test_recommend_method_signature(self):
        """
        Test that the recommend method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.collab_recommender.recommend)
        expected_params = ['user_id', 'tool_name', 'num_recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_get_recommendation_scores_method_signature(self):
        """
        Test that the get_recommendation_scores method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.collab_recommender.get_recommendation_scores)
        expected_params = ['identifier']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_display_recommendations_method_signature(self):
        """
        Test that the display_recommendations method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.collab_recommender.display_recommendations)
        expected_params = ['recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_recommend_method_returns_list_of_dicts(self):
        """
        Test that the recommend method returns a list of dictionaries.
        """
        user_id = 101
        num_recommendations = 1

        # Mock get_recommendation_scores_by_user
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 4.5,
                2: 3.2
            }

            recommendations = self.collab_recommender.recommend(
                user_id=user_id,
                tool_name=None,
                num_recommendations=num_recommendations
            )

            self.assertIsInstance(recommendations, list)
            self.assertIsInstance(recommendations[0], dict)
            self.assertEqual(recommendations[0]['tool_name'], "Beta")

    def test_get_recommendation_scores_returns_dict(self):
        """
        Test that get_recommendation_scores returns a dictionary mapping tool_ids to scores.
        """
        user_id = 102

        # Mock get_recommendation_scores_by_user
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 4.0,
                2: 3.5
            }

            scores = self.collab_recommender.get_recommendation_scores("102")

            mock_get_scores.assert_called_once_with(user_id)

            expected_scores = {
                1: 4.0,
                2: 3.5
            }

            self.assertEqual(scores, expected_scores)

    def test_display_recommendations_handles_empty_list(self):
        """
        Test that display_recommendations correctly handles an empty list.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.collab_recommender.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_display_recommendations_prints_tool_details(self):
        """
        Test that display_recommendations correctly prints tool details.
        """
        recommendations = [
            {
                'tool_id': 2,
                'tool_name': "Beta",
                'category': "Proteomics",
                'features': "mass_spectrometry;protein_identification",
                'cost': 200,
                'description': "Beta Description",
                'url': "http://beta.com",
                'language': "R",
                'platform': "Windows"
            }
        ]

        with patch('builtins.print') as mock_print:
            self.collab_recommender.display_recommendations(recommendations)
            mock_print.assert_any_call("\nRecommended Tools:")
            mock_print.assert_any_call("- Beta - Beta Description (Category: Proteomics, Cost: $200)")

    def test_get_recommendation_scores_with_no_ratings(self):
        """
        Test that get_recommendation_scores returns average ratings when the user has no ratings.
        """
        user_id = 104  # Assume user 104 has no ratings

        # Mock get_recommendation_scores_by_user to return average ratings
        with patch.object(self.collab_recommender, 'get_recommendation_scores_by_user') as mock_get_scores:
            mock_get_scores.return_value = {
                1: 2.5,
                2: 3.5,
                3: 4.0,
                4: 4.5
            }

            scores = self.collab_recommender.get_recommendation_scores("104")

            mock_get_scores.assert_called_once_with(user_id)

            expected_scores = {
                1: 2.5,
                2: 3.5,
                3: 4.0,
                4: 4.5
            }

            self.assertEqual(scores, expected_scores)

    def test_repr_method(self):
        """
        Test the __repr__ method for correct string representation.
        """
        expected_repr = "CollaborativeRecommender(n_neighbors=1, number_of_tools=2)"
        self.assertEqual(repr(self.collab_recommender), expected_repr)


if __name__ == '__main__':
    unittest.main()
