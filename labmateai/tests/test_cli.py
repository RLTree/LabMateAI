import unittest
from unittest.mock import patch, MagicMock
from labmateai.cli import CLI


class TestCLI(unittest.TestCase):

    @patch('labmateai.cli.CLI._load_data_and_initialize_recommenders')
    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    def setUp(self, mock_get_or_create_user, mock_load_data):
        """
        Set up the CLI instance and mock necessary methods before each test.
        """
        # Initialize CLI
        self.cli = CLI()
        # Mock methods
        self.mock_get_or_create_user = mock_get_or_create_user
        self.mock_load_data = mock_load_data

        # Mock recommender for use in tests
        self.cli.recommender = MagicMock()

        # Setup mock tool data
        self.mock_tool_data = [
            MagicMock(
                tool_id=1,
                name="Tool1",
                category="Genomics",
                features="feature1;feature2",
                cost="Free",
                description="Tool1 Description",
                url="http://tool1.com",
                language="Python",
                platform="Linux"
            ),
            MagicMock(
                tool_id=2,
                name="Tool2",
                category="Proteomics",
                features="feature3;feature4",
                cost="Paid",
                description="Tool2 Description",
                url="http://tool2.com",
                language="R",
                platform="Windows"
            )
        ]

    @patch('labmateai.cli.CLI._prompt_rating')
    def test_handle_recommend_similar_tools(self, mock_prompt_rating):
        """
        Test recommending similar tools and prompting for ratings.
        """
        # Mock recommendations returned by the recommender
        self.cli.recommender.recommend_similar_tools.return_value = self.mock_tool_data

        # Simulate user input for tool name
        with patch('builtins.input', side_effect=['Tool1']):
            # Call the method under test
            self.cli.handle_recommend_similar_tools(1)

        # Assert that the recommender was called correctly
        self.cli.recommender.recommend_similar_tools.assert_called_once_with(
            'Tool1')
        # Assert that the rating prompt was called with the correct recommendations
        mock_prompt_rating.assert_called_once_with(self.mock_tool_data, 1)

    @patch('labmateai.cli.CLI._prompt_rating')
    def test_handle_recommend_category_tools(self, mock_prompt_rating):
        """
        Test recommending tools within a specified category and prompting for ratings.
        """
        # Simulate user input for category
        with patch('builtins.input', side_effect=['Genomics']):
            # Assign mock tools to the CLI
            self.cli.tools = self.mock_tool_data
            # Call the method under test
            self.cli.handle_recommend_category_tools(1)

        # Expected recommendations (only tools matching 'Genomics')
        expected_recommendations = [self.mock_tool_data[0]]
        # Assert that the rating prompt was called with the correct recommendations
        mock_prompt_rating.assert_called_once_with(expected_recommendations, 1)

    @patch('labmateai.cli.CLI._prompt_rating')
    def test_handle_search_tools(self, mock_prompt_rating):
        """
        Test searching for tools by keyword and prompting for ratings.
        """
        # Simulate user input for keyword
        with patch('builtins.input', side_effect=['Tool']):
            # Assign mock tools to the CLI
            self.cli.tools = self.mock_tool_data
            # Call the method under test
            self.cli.handle_search_tools(1)

        # Expected recommendations (tools containing 'Tool' in name or description)
        expected_recommendations = self.mock_tool_data
        # Assert that the rating prompt was called with the correct recommendations
        mock_prompt_rating.assert_called_once_with(expected_recommendations, 1)

    @patch('labmateai.cli.CLI._log_interaction')
    def test_prompt_rating_yes(self, mock_log_interaction):
        """
        Test the _prompt_rating method when the user decides to rate a tool.
        """
        # Simulate user inputs: 'yes' to rate, tool ID '1', rating '5', usage frequency 'Often'
        with patch('builtins.input', side_effect=['yes', '1', '5', 'Often']):
            # Call the method under test
            self.cli._prompt_rating(self.mock_tool_data, 1)

        # Assert that the interaction was logged correctly
        mock_log_interaction.assert_called_once_with(
            user_id=1,
            tool_id=1,
            rating=5,
            usage_frequency='Often'
        )

    @patch('labmateai.cli.CLI._log_interaction')
    def test_prompt_rating_no(self, mock_log_interaction):
        """
        Test the _prompt_rating method when the user decides not to rate any tool.
        """
        # Simulate user input: 'no' to not rate any tool
        with patch('builtins.input', side_effect=['no']):
            # Call the method under test
            self.cli._prompt_rating(self.mock_tool_data, 1)

        # Assert that no interaction was logged
        mock_log_interaction.assert_not_called()

    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('builtins.input', create=True)
    @patch('labmateai.cli.CLI.handle_search_tools')
    @patch('labmateai.cli.CLI.handle_recommend_category_tools')
    @patch('labmateai.cli.CLI.handle_recommend_similar_tools')
    def test_menu_choices_recommend_similar_tools_then_exit(
        self, mock_similar, mock_category, mock_search, mock_input, mock_get_user
    ):
        """
        Test CLI menu option 1 (Recommend similar tools) followed by exit.
        """
        # Simulate user selecting option 1, then option 4 to exit
        mock_input.side_effect = ['1', '4']
        # Mock print to suppress actual print statements during testing
        with patch('builtins.print'):
            self.cli.start()

        # Assert that the correct handler was called
        mock_similar.assert_called_once_with(1)
        # Assert that other handlers were not called
        mock_category.assert_not_called()
        mock_search.assert_not_called()

    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('builtins.input', create=True)
    @patch('labmateai.cli.CLI.handle_search_tools')
    @patch('labmateai.cli.CLI.handle_recommend_category_tools')
    @patch('labmateai.cli.CLI.handle_recommend_similar_tools')
    def test_menu_choices_recommend_category_tools_then_exit(
        self, mock_similar, mock_category, mock_search, mock_input, mock_get_user
    ):
        """
        Test CLI menu option 2 (Recommend tools within a category) followed by exit.
        """
        # Simulate user selecting option 2, then option 4 to exit
        mock_input.side_effect = ['2', '4']
        # Mock print to suppress actual print statements during testing
        with patch('builtins.print'):
            self.cli.start()

        # Assert that the correct handler was called
        mock_category.assert_called_once_with(1)
        # Assert that other handlers were not called
        mock_similar.assert_not_called()
        mock_search.assert_not_called()

    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('builtins.input', create=True)
    @patch('labmateai.cli.CLI.handle_search_tools')
    @patch('labmateai.cli.CLI.handle_recommend_category_tools')
    @patch('labmateai.cli.CLI.handle_recommend_similar_tools')
    def test_menu_choices_search_tools_then_exit(
        self, mock_similar, mock_category, mock_search, mock_input, mock_get_user
    ):
        """
        Test CLI menu option 3 (Search tools by keyword) followed by exit.
        """
        # Simulate user selecting option 3, then option 4 to exit
        mock_input.side_effect = ['3', '4']
        # Mock print to suppress actual print statements during testing
        with patch('builtins.print'):
            self.cli.start()

        # Assert that the correct handler was called
        mock_search.assert_called_once_with(1)
        # Assert that other handlers were not called
        mock_similar.assert_not_called()
        mock_category.assert_not_called()

    @patch('labmateai.cli.CLI._get_or_create_user', return_value=1)
    @patch('builtins.input', create=True)
    def test_menu_choices_exit_directly(self, mock_input, mock_get_user):
        """
        Test CLI menu option 4 (Exit) directly.
        """
        # Simulate user selecting option 4 to exit immediately
        mock_input.side_effect = ['4']
        # Mock print to capture exit message
        with patch('builtins.print') as mock_print:
            self.cli.start()

        # Assert that the exit message was printed
        mock_print.assert_any_call("Exiting LabMateAI. Goodbye!")


if __name__ == '__main__':
    unittest.main()
