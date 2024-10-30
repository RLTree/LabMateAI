# labmateai/tests/test_content_based_recommender.py

"""
Test Suite for ContentBasedRecommender Module in LabMateAI.

This test suite ensures that the ContentBasedRecommender class correctly implements the RecommenderInterface
and functions as expected when providing content-based recommendations.
"""

import unittest
from unittest.mock import MagicMock, patch
from labmateai.recommenders.content_based_recommender import ContentBasedRecommender, load_data, build_user_item_matrix
from labmateai.recommenders.recommender_interface import RecommenderInterface
from labmateai.graph import Graph
from labmateai.tree import ToolTree
from labmateai.tool import Tool
import pandas as pd


class TestContentBasedRecommender(unittest.TestCase):
    """
    Test cases for the ContentBasedRecommender class.
    """

    def setUp(self):
        """
        Set up the ContentBasedRecommender instance with mocked Graph and ToolTree.
        This setup runs before each test to ensure test isolation.
        """
        # Create sample Tool objects
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            features=["sequence_analysis", "alignment"],
            cost=100,
            description="Alpha Description",
            url="http://alpha.com",
            language="Python",
            platform="Linux"
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            features=["mass_spectrometry", "protein_identification"],
            cost=200,
            description="Beta Description",
            url="http://beta.com",
            language="R",
            platform="Windows"
        )
        self.tool3 = Tool(
            tool_id=3,
            name="Gamma",
            category="Genomics",
            features=["variant_calling", "genome_assembly"],
            cost=150,
            description="Gamma Description",
            url="http://gamma.com",
            language="Java",
            platform="Mac"
        )
        self.tool4 = Tool(
            tool_id=4,
            name="Delta",
            category="Metabolomics",
            features=["metabolite_profiling", "pathway_analysis"],
            cost=120,
            description="Delta Description",
            url="http://delta.com",
            language="Python",
            platform="Linux"
        )
        self.tools = [self.tool1, self.tool2, self.tool3, self.tool4]

        # Mock Graph and ToolTree
        self.mock_graph = MagicMock(spec=Graph)
        self.mock_tool_tree = MagicMock(spec=ToolTree)

        # Sample tools DataFrame for content-based recommender
        self.tools_df_data = {
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
        self.tools_df = pd.DataFrame(self.tools_df_data)

        # Initialize ContentBasedRecommender with mocks
        self.cbr = ContentBasedRecommender(
            tools=self.tools,
            graph=self.mock_graph,
            tree=self.mock_tool_tree
        )

    def test_initialization_with_valid_tools(self):
        """
        Test that ContentBasedRecommender initializes correctly with a valid list of tools.
        """
        self.assertEqual(len(self.cbr.tools), 4)
        self.mock_graph.build_graph.assert_called_once_with(self.tools)
        self.mock_tool_tree.build_tree.assert_called_once_with(self.tools)
        self.assertIsNotNone(self.cbr.similarity_matrix)
        self.assertIsNotNone(self.cbr.vectorizer)

    def test_initialization_with_duplicate_tool_ids(self):
        """
        Test that initializing ContentBasedRecommender with duplicate tool IDs raises ValueError.
        """
        duplicate_tool = Tool(
            tool_id=1,
            name="Epsilon",
            category="Genomics",
            features=["gene_expression"],
            cost=130,
            description="Epsilon Description",
            url="http://epsilon.com",
            language="C++",
            platform="Linux"
        )
        tools_with_duplicate = self.tools + [duplicate_tool]

        with self.assertRaises(ValueError) as context:
            ContentBasedRecommender(
                tools=tools_with_duplicate,
                graph=self.mock_graph,
                tree=self.mock_tool_tree
            )
        self.assertIn("Tool 'Epsilon' already exists in the dataset.", str(context.exception))

    def test_recommend_valid_tool_name(self):
        """
        Test that recommend method returns correct recommendations based on a valid tool name.
        """
        tool_name = "Alpha"
        num_recommendations = 2

        # Mock graph.find_most_relevant_tools to return tool3 and tool2
        self.mock_graph.find_most_relevant_tools.return_value = [self.tool3, self.tool2]

        # Call the recommend method
        recommendations = self.cbr.recommend(
            user_id=None,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        # Assert that find_most_relevant_tools was called correctly
        self.mock_graph.find_most_relevant_tools.assert_called_once_with(
            start_tool=self.tool1,
            num_recommendations=num_recommendations
        )

        # Assert that recommendations are as expected
        expected_recommendations = [self.tool3.__dict__, self.tool2.__dict__]
        self.assertEqual(recommendations, expected_recommendations)

    def test_recommend_invalid_tool_name(self):
        """
        Test that recommend method raises ValueError when the tool name is not found.
        """
        tool_name = "Zeta"
        num_recommendations = 2

        with self.assertRaises(ValueError) as context:
            self.cbr.recommend(
                user_id=None,
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        self.assertIn(f"Tool '{tool_name}' not found in the dataset.", str(context.exception))
        self.mock_graph.find_most_relevant_tools.assert_not_called()

    def test_recommend_no_tool_name_provided(self):
        """
        Test that recommend method returns an empty list when no tool_name or user_id is provided.
        """
        with self.assertRaises(ValueError) as context:
            self.cbr.recommend(
                user_id=None,
                tool_name=None,
                num_recommendations=3
            )
        self.assertIn("At least one of user_id or tool_name must be provided for recommendations.", str(context.exception))

    def test_recommend_num_recommendations_less_than_one(self):
        """
        Test that recommend method raises ValueError when num_recommendations is less than 1.
        """
        with self.assertRaises(ValueError) as context:
            self.cbr.recommend(
                user_id=None,
                tool_name="Alpha",
                num_recommendations=0
            )
        self.assertIn("num_recommendations must be at least 1.", str(context.exception))
        self.mock_graph.find_most_relevant_tools.assert_not_called()

    def test_get_recommendation_scores_valid_tool(self):
        """
        Test that get_recommendation_scores returns correct similarity scores for a valid tool.
        """
        tool_name = "Alpha"

        # Mock similarity_matrix for tool1 (Alpha)
        # Assuming similarity_matrix index 0 corresponds to tool1
        self.cbr.similarity_matrix = pd.DataFrame(
            [
                [1.0, 0.8, 0.6, 0.4],
                [0.8, 1.0, 0.7, 0.5],
                [0.6, 0.7, 1.0, 0.9],
                [0.4, 0.5, 0.9, 1.0]
            ]
        )

        # Call get_recommendation_scores
        scores = self.cbr.get_recommendation_scores(tool_name)

        # Expected scores (excluding the tool itself)
        expected_scores = {
            2: 0.8,
            3: 0.6,
            4: 0.4
        }

        self.assertEqual(scores, expected_scores)

    def test_get_recommendation_scores_invalid_tool(self):
        """
        Test that get_recommendation_scores raises ValueError when the tool name is not found.
        """
        tool_name = "Eta"

        with self.assertRaises(ValueError) as context:
            self.cbr.get_recommendation_scores(tool_name)
        self.assertIn(f"Tool '{tool_name}' not found in the dataset.", str(context.exception))

    def test_display_recommendations_with_results(self):
        """
        Test that display_recommendations method correctly prints the recommended tools.
        """
        recommendations = [
            {'tool_id': 3, 'name': "Gamma", 'category': "Genomics", 'features': "variant_calling;genome_assembly",
             'cost': 150, 'description': "Gamma Description", 'url': "http://gamma.com", 'language': "Java",
             'platform': "Mac"},
            {'tool_id': 2, 'name': "Beta", 'category': "Proteomics", 'features': "mass_spectrometry;protein_identification",
             'cost': 200, 'description': "Beta Description", 'url': "http://beta.com", 'language': "R",
             'platform': "Windows"}
        ]

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_any_call("\nRecommended Tools:")
            mock_print.assert_any_call("- Gamma - Gamma Description (Category: Genomics, Cost: $150)")
            mock_print.assert_any_call("- Beta - Beta Description (Category: Proteomics, Cost: $200)")

    def test_display_recommendations_no_results(self):
        """
        Test that display_recommendations method correctly handles empty recommendations.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_get_recommendation_scores_with_no_similarity_matrix(self):
        """
        Test that get_recommendation_scores returns an empty dictionary when similarity_matrix is None.
        """
        self.cbr.similarity_matrix = None
        tool_name = "Alpha"

        scores = self.cbr.get_recommendation_scores(tool_name)
        self.assertEqual(scores, {})

    def test_recommend_tool_not_found_after_initial_check(self):
        """
        Test that recommend_similar_tools raises ValueError when the tool is not found after initial check.
        """
        tool_name = "Alpha"

        # Mock graph.find_most_relevant_tools to return an empty list
        self.mock_graph.find_most_relevant_tools.return_value = []

        # Force the selected_tool to None after initial check
        with patch.object(self.cbr, 'tools', new=[]):
            with self.assertRaises(ValueError) as context:
                self.cbr.recommend_similar_tools(tool_name=tool_name, num_recommendations=2)
            self.assertIn(f"Tool '{tool_name}' not found after initial check.", str(context.exception))

    def test_repr_method(self):
        """
        Test the __repr__ method for correct string representation.
        """
        expected_repr = (
            f"ContentBasedRecommender(tools=4, "
            f"graph={repr(self.mock_graph)}, tree={repr(self.mock_tool_tree)})"
        )
        self.assertEqual(repr(self.cbr), expected_repr)


class TestRecommenderInterfaceCompliance(unittest.TestCase):
    """
    Test cases to ensure that ContentBasedRecommender complies with RecommenderInterface.
    """

    def setUp(self):
        """
        Set up a mock ContentBasedRecommender instance.
        """
        # Mock tools
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            features=["sequence_analysis", "alignment"],
            cost=100,
            description="Alpha Description",
            url="http://alpha.com",
            language="Python",
            platform="Linux"
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            features=["mass_spectrometry", "protein_identification"],
            cost=200,
            description="Beta Description",
            url="http://beta.com",
            language="R",
            platform="Windows"
        )
        self.tools = [self.tool1, self.tool2]

        # Mock Graph and ToolTree
        self.mock_graph = MagicMock(spec=Graph)
        self.mock_tool_tree = MagicMock(spec=ToolTree)

        # Initialize ContentBasedRecommender with mocks
        self.cbr = ContentBasedRecommender(
            tools=self.tools,
            graph=self.mock_graph,
            tree=self.mock_tool_tree
        )

    def test_interface_methods_exist(self):
        """
        Test that ContentBasedRecommender implements all methods defined in RecommenderInterface.
        """
        self.assertTrue(hasattr(self.cbr, 'recommend'))
        self.assertTrue(hasattr(self.cbr, 'get_recommendation_scores'))
        self.assertTrue(hasattr(self.cbr, 'display_recommendations'))
        self.assertTrue(hasattr(self.cbr, '__repr__'))

    def test_recommend_method_signature(self):
        """
        Test that the recommend method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.recommend)
        expected_params = ['user_id', 'tool_name', 'num_recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_get_recommendation_scores_method_signature(self):
        """
        Test that the get_recommendation_scores method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.get_recommendation_scores)
        expected_params = ['identifier']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_display_recommendations_method_signature(self):
        """
        Test that the display_recommendations method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.display_recommendations)
        expected_params = ['recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_recommend_method_returns_list_of_dicts(self):
        """
        Test that the recommend method returns a list of dictionaries.
        """
        tool_name = "Alpha"
        num_recommendations = 1
        self.mock_graph.find_most_relevant_tools.return_value = [self.tool2]

        recommendations = self.cbr.recommend(
            user_id=None,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        self.assertIsInstance(recommendations, list)
        self.assertIsInstance(recommendations[0], dict)
        self.assertEqual(recommendations[0]['name'], "Beta")

    def test_get_recommendation_scores_returns_dict(self):
        """
        Test that get_recommendation_scores returns a dictionary mapping tool_ids to scores.
        """
        tool_name = "Alpha"
        self.cbr.similarity_matrix = pd.DataFrame(
            [
                [1.0, 0.8],
                [0.8, 1.0]
            ]
        )
        scores = self.cbr.get_recommendation_scores(tool_name)
        expected_scores = {2: 0.8}
        self.assertEqual(scores, expected_scores)

    def test_display_recommendations_handles_empty_list(self):
        """
        Test that display_recommendations correctly handles an empty list.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_display_recommendations_prints_tool_details(self):
        """
        Test that display_recommendations correctly prints tool details.
        """
        recommendations = [
            {'tool_id': 2, 'name': "Beta", 'category': "Proteomics", 'features': "mass_spectrometry;protein_identification",
             'cost': 200, 'description': "Beta Description", 'url': "http://beta.com", 'language': "R",
             'platform': "Windows"}
        ]

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_any_call("\nRecommended Tools:")
            mock_print.assert_any_call(
                "- Beta - Beta Description (Category: Proteomics, Cost: $200)"
            )

    def test_get_recommendation_scores_with_no_similarity_matrix(self):
        """
        Test that get_recommendation_scores returns an empty dictionary when similarity_matrix is None.
        """
        self.cbr.similarity_matrix = None
        tool_name = "Alpha"

        scores = self.cbr.get_recommendation_scores(tool_name)
        self.assertEqual(scores, {})

    def test_recommend_with_tool_name_not_in_dataset(self):
        """
        Test that recommend raises ValueError when the tool name is not in the dataset.
        """
        tool_name = "Zeta"
        num_recommendations = 2

        with self.assertRaises(ValueError) as context:
            self.cbr.recommend(
                user_id=None,
                tool_name=tool_name,
                num_recommendations=num_recommendations
            )
        self.assertIn(f"Tool '{tool_name}' not found in the dataset.", str(context.exception))
        self.mock_graph.find_most_relevant_tools.assert_not_called()


class TestContentBasedRecommenderInterfaceCompliance(unittest.TestCase):
    """
    Test cases to ensure that ContentBasedRecommender complies with RecommenderInterface.
    """

    def setUp(self):
        """
        Set up a mock ContentBasedRecommender instance.
        """
        # Mock tools
        self.tool1 = Tool(
            tool_id=1,
            name="Alpha",
            category="Genomics",
            features=["sequence_analysis", "alignment"],
            cost=100,
            description="Alpha Description",
            url="http://alpha.com",
            language="Python",
            platform="Linux"
        )
        self.tool2 = Tool(
            tool_id=2,
            name="Beta",
            category="Proteomics",
            features=["mass_spectrometry", "protein_identification"],
            cost=200,
            description="Beta Description",
            url="http://beta.com",
            language="R",
            platform="Windows"
        )
        self.tools = [self.tool1, self.tool2]

        # Mock Graph and ToolTree
        self.mock_graph = MagicMock(spec=Graph)
        self.mock_tool_tree = MagicMock(spec=ToolTree)

        # Initialize ContentBasedRecommender with mocks
        self.cbr = ContentBasedRecommender(
            tools=self.tools,
            graph=self.mock_graph,
            tree=self.mock_tool_tree
        )

    def test_interface_methods_exist(self):
        """
        Test that ContentBasedRecommender implements all methods defined in RecommenderInterface.
        """
        self.assertTrue(hasattr(self.cbr, 'recommend'))
        self.assertTrue(hasattr(self.cbr, 'get_recommendation_scores'))
        self.assertTrue(hasattr(self.cbr, 'display_recommendations'))
        self.assertTrue(hasattr(self.cbr, '__repr__'))

    def test_recommend_method_signature(self):
        """
        Test that the recommend method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.recommend)
        expected_params = ['user_id', 'tool_name', 'num_recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_get_recommendation_scores_method_signature(self):
        """
        Test that the get_recommendation_scores method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.get_recommendation_scores)
        expected_params = ['identifier']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_display_recommendations_method_signature(self):
        """
        Test that the display_recommendations method has the correct signature.
        """
        from inspect import signature
        sig = signature(self.cbr.display_recommendations)
        expected_params = ['recommendations']
        self.assertEqual(list(sig.parameters.keys()), expected_params)

    def test_recommend_method_returns_list_of_dicts(self):
        """
        Test that the recommend method returns a list of dictionaries.
        """
        tool_name = "Alpha"
        num_recommendations = 1
        self.mock_graph.find_most_relevant_tools.return_value = [self.tool2]

        recommendations = self.cbr.recommend(
            user_id=None,
            tool_name=tool_name,
            num_recommendations=num_recommendations
        )

        self.assertIsInstance(recommendations, list)
        self.assertIsInstance(recommendations[0], dict)
        self.assertEqual(recommendations[0]['name'], "Beta")

    def test_get_recommendation_scores_returns_dict(self):
        """
        Test that get_recommendation_scores returns a dictionary mapping tool_ids to scores.
        """
        tool_name = "Alpha"
        self.cbr.similarity_matrix = pd.DataFrame(
            [
                [1.0, 0.8],
                [0.8, 1.0]
            ]
        )
        scores = self.cbr.get_recommendation_scores(tool_name)
        expected_scores = {2: 0.8}
        self.assertEqual(scores, expected_scores)

    def test_display_recommendations_handles_empty_list(self):
        """
        Test that display_recommendations correctly handles an empty list.
        """
        recommendations = []

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_called_once_with("No recommendations found.")

    def test_display_recommendations_prints_tool_details(self):
        """
        Test that display_recommendations correctly prints tool details.
        """
        recommendations = [
            {'tool_id': 2, 'name': "Beta", 'category': "Proteomics", 'features': "mass_spectrometry;protein_identification",
             'cost': 200, 'description': "Beta Description", 'url': "http://beta.com", 'language': "R",
             'platform': "Windows"}
        ]

        with patch('builtins.print') as mock_print:
            self.cbr.display_recommendations(recommendations)
            mock_print.assert_any_call("\nRecommended Tools:")
            mock_print.assert_any_call(
                "- Beta - Beta Description (Category: Proteomics, Cost: $200)"
            )

    def test_get_recommendation_scores_with_no_similarity_matrix(self):
        """
        Test that get_recommendation_scores returns an empty dictionary when similarity_matrix is None.
        """
        self.cbr.similarity_matrix = None
        tool_name = "Alpha"

        scores = self.cbr.get_recommendation_scores(tool_name)
        self.assertEqual(scores, {})

    def test_recommend_tool_not_found_after_initial_check(self):
        """
        Test that recommend_similar_tools raises ValueError when the tool is not found after initial check.
        """
        tool_name = "Alpha"

        # Mock graph.find_most_relevant_tools to return an empty list
        self.mock_graph.find_most_relevant_tools.return_value = []

        # Force the selected_tool to None after initial check
        with patch.object(self.cbr, 'tools', new=[]):
            with self.assertRaises(ValueError) as context:
                self.cbr.recommend_similar_tools(tool_name=tool_name, num_recommendations=2)
            self.assertIn(f"Tool '{tool_name}' not found after initial check.", str(context.exception))


if __name__ == '__main__':
    unittest.main()
