# labmateai/tests/test_cli.py

"""
Test Suite for the CLI Module in LabMateAI.

This test suite ensures that the CLI class functions correctly,
covering various scenarios including user interactions, database operations,
error handling, and integration with recommender systems.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import sys
import os

# Import the CLI class from cli.py
from labmateai.cli import CLI

# Define a simple Tool class for testing purposes
class Tool:
    """
    A mock Tool class for testing purposes.
    """
    def __init__(self, tool_id, name, category, description, features, cost, url, language, platform):
        self.tool_id = tool_id
        self.name = name
        self.category = category
        self.description = description
        self.features = features
        self.cost = cost
        self.url = url
        self.language = language
        self.platform = platform

class TestCLI(unittest.TestCase):
    """
    Test cases for the CLI class.
    """

    def setUp(self):
        """
        Set up a CLI instance with mocked database components for testing.
        """
        # Set the TESTING environment variable
        os.environ['TESTING'] = 'True'

        # Patch the database engine and session maker
        self.patcher_engine = patch('labmateai.cli.CLI._get_engine')
        self.mock_get_engine = self.patcher_engine.start()

        self.patcher_session_maker = patch('labmateai.cli.CLI._get_session_maker')
        self.mock_get_session_maker = self.patcher_session_maker.start()
        self.mock_session_maker = MagicMock()
        self.mock_get_session_maker.return_value = self.mock_session_maker
        self.mock_session = MagicMock()
        self.mock_session_maker.return_value = self.mock_session

        # Patch the run_migrations method
        self.patcher_run_migrations = patch('labmateai.cli.CLI._run_migrations')
        self.mock_run_migrations = self.patcher_run_migrations.start()

        # Initialize CLI instance
        self.cli = CLI(testing=True)

    def tearDown(self):
        """
        Stop all patches.
        """
        patch.stopall()

    def test_construct_database_url_testing(self):
        """
        Test that the database URL is constructed correctly in testing mode.
        """
        url = self.cli._construct_database_url()
        self.assertEqual(url, 'sqlite:///:memory:')

    def test_construct_database_url_production(self):
        """
        Test that the database URL is constructed correctly in production mode.
        """
        if 'TESTING' in os.environ:
            del os.environ['TESTING']
        self.cli.testing = False
        self.cli.db_config = {
            'dbname': 'dbname',
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port'
        }
        url = self.cli._construct_database_url()
        expected_url = 'postgresql://user:password@host:port/dbname'
        self.assertEqual(url, expected_url)

    @patch('labmateai.cli.input', side_effect=['test@example.com'])
    def test_get_or_create_user_existing(self, mock_input):
        """
        Test getting an existing user.
        """
        from labmateai.models import User

        # Mock the session's query method
        mock_user = User(user_id=1, user_name='Test User', email='test@example.com', department='Dept', role='Role')
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        user_id = self.cli._get_or_create_user()
        self.assertEqual(user_id, 1)
        self.mock_session.query.assert_called()

    @patch('labmateai.cli.input', side_effect=['new@example.com', 'New User', 'Dept', 'Role'])
    def test_get_or_create_user_new(self, mock_input):
        """
        Test creating a new user.
        """
        from labmateai.models import User

        # Mock the session's query method to return None
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = None

        # Mock the session's add and commit methods
        self.mock_session.add = MagicMock()
        self.mock_session.commit = MagicMock()
        self.mock_session.refresh = MagicMock()

        # Define the side effect to assign user_id
        def refresh_side_effect(user):
            user.user_id = 1  # Assign a mock user_id

        # Assign the side effect without calling the function
        self.mock_session.refresh.side_effect = refresh_side_effect

        user_id = self.cli._get_or_create_user()
        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, 1)
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once()

    def test_log_interaction(self):
        """
        Test logging an interaction.
        """
        from labmateai.models import Interaction

        self.cli._log_interaction(user_id=1, tool_id=1, rating=5, usage_frequency='Often')
        self.mock_session.add.assert_called()
        self.mock_session.commit.assert_called_once()

    def test_log_interaction_exception(self):
        """
        Test logging an interaction with an exception.
        """
        self.mock_session.add.side_effect = Exception("Database Error")
        with patch('labmateai.cli.print') as mock_print:
            self.cli._log_interaction(user_id=1, tool_id=1)
            mock_print.assert_called_with("An error occurred while logging your interaction. Please try again.")

    @patch('labmateai.cli.input', side_effect=[''])
    def test_get_number_of_recommendations_default(self, mock_input):
        """
        Test getting the default number of recommendations.
        """
        num = self.cli._get_number_of_recommendations()
        self.assertEqual(num, 3)

    @patch('labmateai.cli.input', side_effect=['5'])
    def test_get_number_of_recommendations_custom(self, mock_input):
        """
        Test getting a custom number of recommendations.
        """
        num = self.cli._get_number_of_recommendations()
        self.assertEqual(num, 5)

    @patch('labmateai.cli.input', side_effect=['invalid', '5'])
    def test_get_number_of_recommendations_invalid(self, mock_input):
        """
        Test handling invalid input for the number of recommendations.
        """
        with patch('labmateai.cli.print') as mock_print:
            num = self.cli._get_number_of_recommendations()
            self.assertEqual(num, 5)
            mock_print.assert_called_with("Please enter a positive integer.")

    @patch('labmateai.cli.CLI._load_data_and_initialize_recommenders')
    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('labmateai.cli.input', side_effect=['4'])
    def test_start_exit(self, mock_input, mock_get_user, mock_load_data):
        """
        Test exiting the CLI.
        """
        with patch('labmateai.cli.print') as mock_print:
            with self.assertRaises(SystemExit):
                self.cli.start()
            mock_print.assert_called_with("Exiting LabMateAI. Goodbye!")

    @patch('labmateai.cli.CLI.handle_recommend_similar_tools')
    @patch('labmateai.cli.CLI._load_data_and_initialize_recommenders')
    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('labmateai.cli.input', side_effect=['1', '4'])
    def test_start_recommend_similar_tools(self, mock_input, mock_get_user, mock_load_data, mock_handle):
        """
        Test selecting recommend similar tools.
        """
        with self.assertRaises(SystemExit):
            self.cli.start()
        mock_handle.assert_called_once_with(1)

    @patch('labmateai.cli.CLI.handle_recommend_category_tools')
    @patch('labmateai.cli.CLI._load_data_and_initialize_recommenders')
    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('labmateai.cli.input', side_effect=['2', '4'])
    def test_start_recommend_category_tools(self, mock_input, mock_get_user, mock_load_data, mock_handle):
        """
        Test selecting recommend category tools.
        """
        with self.assertRaises(SystemExit):
            self.cli.start()
        mock_handle.assert_called_once_with(1)

    @patch('labmateai.cli.CLI.handle_search_tools')
    @patch('labmateai.cli.CLI._load_data_and_initialize_recommenders')
    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('labmateai.cli.input', side_effect=['3', '4'])
    def test_start_search_tools(self, mock_input, mock_get_user, mock_load_data, mock_handle):
        """
        Test selecting search tools.
        """
        with self.assertRaises(SystemExit):
            self.cli.start()
        mock_handle.assert_called_once_with(1)

    @patch('labmateai.cli.input', side_effect=['yes', '1', '5', 'Often', 'no'])
    def test_prompt_rating(self, mock_input):
        """
        Test prompting the user for rating.
        """
        recommendations = [
            Tool(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux')
        ]
        with patch.object(self.cli, '_log_interaction') as mock_log:
            self.cli._prompt_rating(recommendations, user_id=1)
            mock_log.assert_called_once_with(user_id=1, tool_id=1, rating=5, usage_frequency='Often')

    @patch('labmateai.cli.input', side_effect=['yes', 'invalid', 'yes', '1', '5', 'Often', 'no'])
    def test_prompt_rating_invalid_tool_id(self, mock_input):
        """
        Test prompting the user for rating with invalid tool ID.
        """
        recommendations = [
            Tool(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux')
        ]
        with patch.object(self.cli, '_log_interaction') as mock_log:
            with patch('labmateai.cli.print') as mock_print:
                self.cli._prompt_rating(recommendations, user_id=1)
                mock_log.assert_called_once()
                mock_input.assert_any_call("Would you like to rate any of these tools? (yes/no): ")
                mock_input.assert_any_call("Enter the Tool ID you want to rate: ")
                mock_print.assert_any_call("Invalid Tool ID. Please enter a numeric value: ")

    @patch('labmateai.cli.input', side_effect=['invalid_choice', 'yes', '1', '5', 'Often', 'no'])
    def test_prompt_rating_invalid_choice(self, mock_input):
        """
        Test prompting the user for rating with invalid initial choice.
        """
        recommendations = [
            Tool(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux')
        ]
        with patch.object(self.cli, '_log_interaction') as mock_log:
            with patch('labmateai.cli.print') as mock_print:
                self.cli._prompt_rating(recommendations, user_id=1)
                mock_log.assert_called_once()
                mock_print.assert_any_call("Please respond with 'yes' or 'no'.")

    @patch('labmateai.cli.CLI._prompt_rating')
    @patch('labmateai.cli.input', side_effect=['Tool1', '3'])
    def test_handle_recommend_similar_tools(self, mock_input, mock_prompt):
        """
        Test handling recommend similar tools.
        """
        # Mock the recommender
        self.cli.recommender = MagicMock()
        recommendations = [
            Tool(tool_id=2, name='Tool2', category='Category1', description='Desc2',
                 features=['feature2'], cost='Free', url='url2', language='Python', platform='Linux')
        ]
        self.cli.recommender.recommend_similar_tools.return_value = recommendations

        with patch('labmateai.cli.print') as mock_print:
            self.cli.handle_recommend_similar_tools(user_id=1)
            mock_print.assert_any_call("\nRecommendations:")
            mock_prompt.assert_called_once_with(recommendations, 1)

    @patch('labmateai.cli.CLI._prompt_rating')
    @patch('labmateai.cli.input', side_effect=['Category1', '3'])
    def test_handle_recommend_category_tools(self, mock_input, mock_prompt):
        """
        Test handling recommend category tools.
        """
        # Mock the tools
        self.cli.tools = [
            Tool(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux'),
            Tool(tool_id=2, name='Tool2', category='Category2', description='Desc2',
                 features=['feature2'], cost='Free', url='url2', language='Python', platform='Linux')
        ]

        with patch('labmateai.cli.print') as mock_print:
            self.cli.handle_recommend_category_tools(user_id=1)
            mock_print.assert_any_call("\nRecommendations:")
            mock_prompt.assert_called_once()

    @patch('labmateai.cli.CLI._prompt_rating')
    @patch('labmateai.cli.input', side_effect=['keyword', '3'])
    def test_handle_search_tools(self, mock_input, mock_prompt):
        """
        Test handling search tools.
        """
        # Mock the tools
        self.cli.tools = [
            Tool(tool_id=1, name='Keyword Tool', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux'),
            Tool(tool_id=2, name='Tool2', category='Category2', description='Desc2',
                 features=['feature2'], cost='Free', url='url2', language='Python', platform='Linux')
        ]

        with patch('labmateai.cli.print') as mock_print:
            self.cli.handle_search_tools(user_id=1)
            mock_print.assert_any_call("\nSearch Results:")
            mock_prompt.assert_called_once()

    @patch('labmateai.cli.CLI._prompt_rating')
    @patch('labmateai.cli.input', side_effect=['unknown', '3'])
    def test_handle_search_tools_no_results(self, mock_input, mock_prompt):
        """
        Test handling search tools with no results.
        """
        # Mock the tools
        self.cli.tools = [
            Tool(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                 features=['feature1'], cost='Free', url='url1', language='Python', platform='Linux')
        ]

        with patch('labmateai.cli.print') as mock_print:
            self.cli.handle_search_tools(user_id=1)
            mock_print.assert_any_call("No tools found for the given keyword.")
            mock_prompt.assert_not_called()

    def test_load_data_and_initialize_recommenders(self):
        """
        Test loading data and initializing recommenders.
        """
        # Mock the session's query method to return tools
        from labmateai.models import Tool as ToolModel, Interaction

        tool1 = ToolModel(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                          features='{feature1}', cost='Free', url='url1', language='Python', platform='Linux')
        tool2 = ToolModel(tool_id=2, name='Tool2', category='Category2', description='Desc2',
                          features='{feature2}', cost='Free', url='url2', language='Python', platform='Linux')

        self.mock_session.query.return_value.all.return_value = [tool1, tool2]

        # Mock interactions
        interaction = Interaction(user_id=1, tool_id=1, rating=5, usage_frequency='Often')
        self.mock_session.query.return_value.filter.return_value.all.return_value = [interaction]

        # Mock recommenders
        with patch('labmateai.recommenders.content_based_recommender.ContentBasedRecommender') as mock_cb_recommender, \
             patch('labmateai.recommenders.collaborative_recommender.CollaborativeRecommender') as mock_cf_recommender, \
             patch('labmateai.recommenders.hybrid_recommender.HybridRecommender') as mock_hybrid_recommender:

            self.cli._load_data_and_initialize_recommenders()
            self.assertTrue(self.cli.data_loaded)
            mock_cb_recommender.assert_called_once()
            mock_cf_recommender.assert_called_once()
            mock_hybrid_recommender.assert_called_once()

    def test_load_data_and_initialize_recommenders_no_interactions(self):
        """
        Test loading data when there are no interactions.
        """
        # Mock the session's query method to return tools
        from labmateai.models import Tool as ToolModel

        tool1 = ToolModel(tool_id=1, name='Tool1', category='Category1', description='Desc1',
                          features='{feature1}', cost='Free', url='url1', language='Python', platform='Linux')

        self.mock_session.query.return_value.all.return_value = [tool1]

        # Mock interactions to be empty
        self.mock_session.query.return_value.filter.return_value.all.return_value = []

        # Mock recommenders
        with patch('labmateai.recommenders.content_based_recommender.ContentBasedRecommender') as mock_cb_recommender, \
             patch('labmateai.cli.logging') as mock_logging:

            self.cli._load_data_and_initialize_recommenders()
            self.assertTrue(self.cli.data_loaded)
            mock_cb_recommender.assert_called_once()
            mock_logging.warning.assert_any_call("No interactions found in the database.")

    def test_load_data_and_initialize_recommenders_exception(self):
        """
        Test handling exceptions during data loading.
        """
        self.mock_session.query.side_effect = Exception("Database Error")

        with patch('labmateai.cli.print') as mock_print:
            with self.assertRaises(SystemExit):
                self.cli._load_data_and_initialize_recommenders()
            mock_print.assert_called_with("Failed to initialize the application. Please ensure the database is set up correctly.")

    @patch('labmateai.cli.print')
    def test_handle_recommend_similar_tools_exception(self, mock_print):
        """
        Test handling exceptions in recommend similar tools.
        """
        self.cli.recommender = MagicMock()
        self.cli.recommender.recommend_similar_tools.side_effect = Exception("Error")
        self.cli.handle_recommend_similar_tools(user_id=1)
        mock_print.assert_called_with("An error occurred while fetching recommendations. Please try again.")

    @patch('labmateai.cli.print')
    def test_handle_recommend_category_tools_exception(self, mock_print):
        """
        Test handling exceptions in recommend category tools.
        """
        self.cli.tools = None  # Simulate tools not loaded
        self.cli.handle_recommend_category_tools(user_id=1)
        mock_print.assert_called_with("An error occurred while fetching recommendations. Please try again.")

    @patch('labmateai.cli.print')
    def test_handle_search_tools_exception(self, mock_print):
        """
        Test handling exceptions in search tools.
        """
        self.cli.tools = None  # Simulate tools not loaded
        self.cli.handle_search_tools(user_id=1)
        mock_print.assert_called_with("An error occurred while searching for tools. Please try again.")

    def test_main(self):
        """
        Test the main function.
        """
        with patch('labmateai.cli.CLI.start') as mock_start:
            with patch('labmateai.cli.CLI.__init__', return_value=None):
                from labmateai.cli import main
                main()
                mock_start.assert_called_once()

if __name__ == '__main__':
    unittest.main()
