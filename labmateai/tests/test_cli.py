# Updated test_cli.py

import pytest
from unittest.mock import patch, MagicMock, call
from labmateai.cli import CLI


@patch('psycopg2.connect')
def test_user_signup(mock_connect):
    """
    Test the signup process for a new user.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  # Adjusted here

    # Mock cursor behavior for no user found and insertion
    mock_cursor.fetchone.side_effect = [None, (1,)]
    mock_cursor.execute.return_value = None  # For insertion

    cli = CLI()

    with patch('builtins.input', side_effect=[
        'johndoe@example.com',  # Email input
        'John Doe',             # Full name input
        'Biology',              # Department input
        'Researcher',           # Role input
        '5'                     # Choice to exit
    ]):
        cli.start()

    # Assert that a new user was added to the database
    insert_query = "INSERT INTO users (user_name, email, department, role)"
    assert any(insert_query in str(
        call[0][0]) for call in mock_cursor.execute.call_args_list), "User insertion query not found."


@patch('psycopg2.connect')
def test_recommend_tools_in_category(mock_connect):
    """
    Test recommending tools within a specified category.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  # Adjusted here

    # Mock cursor behavior for loading tools
    mock_cursor.fetchall.side_effect = [
        [  # First fetchall for loading tools
            (1, 'Seurat', 'Single-Cell Analysis', 'feature1;feature2',
             'Free', 'Description', 'http://example.com', 'Python', 'Linux')
        ],
        []  # Second fetchall for interactions (empty)
    ]

    cli = CLI()

    # Include email as the first input
    with patch('builtins.input', side_effect=['johndoe@example.com', '2', 'Single-Cell Analysis', '5']):
        with patch('builtins.print') as mock_print:
            cli.start()
            # Assert that recommendations were printed
            assert any("Recommendations:" in ''.join(map(str, call.args))
                       for call in mock_print.call_args_list), "Category recommendations not printed."


@patch('psycopg2.connect')
def test_search_tools_by_keyword(mock_connect):
    """
    Test searching tools by a keyword.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  # Adjusted here

    # Mock cursor behavior for loading tools
    mock_cursor.fetchall.side_effect = [
        [  # First fetchall for loading tools
            (1, 'RNA Tool', 'Genomics', 'feature1;feature2', 'Free',
             'Description', 'http://example.com', 'Python', 'Linux')
        ],
        []  # Second fetchall for interactions (empty)
    ]

    cli = CLI()

    # Include email as the first input
    with patch('builtins.input', side_effect=['johndoe@example.com', '3', 'RNA', '5']):
        with patch('builtins.print') as mock_print:
            cli.start()
            # Assert that search results were printed
            assert any("Search Results:" in ''.join(map(str, call.args))
                       for call in mock_print.call_args_list), "Search results not printed."


@patch('psycopg2.connect')
def test_rate_recommendation(mock_connect):
    """
    Test rating a recommended tool.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor  # Adjusted here

    # Mock cursor behavior for loading tools and interactions
    mock_cursor.fetchall.side_effect = [
        [  # First fetchall for loading tools
            (101, 'Some Tool', 'Chemistry', 'featureA;featureB',
             'Free', 'A useful tool', 'http://example.com', 'Python', 'Linux')
        ],
        []  # Second fetchall for interactions (empty)
    ]
    # Mock cursor behavior for user lookup
    mock_cursor.fetchone.side_effect = [
        (1, 'Jane Doe', 'janedoe@example.com', 'Chemistry', 'Student')
    ]

    cli = CLI()

    # Include email as the first input and an extra '5' to exit
    with patch('builtins.input', side_effect=['janedoe@example.com', '4', '101', '5', '5']):
        cli.start()

    # Assert the rating insertion
    insert_query = "INSERT INTO interactions (user_id, tool_id, rating, usage_frequency, timestamp)"
    assert any(insert_query in str(
        call.args[0]) for call in mock_cursor.execute.call_args_list), "Interaction insertion query not found."
