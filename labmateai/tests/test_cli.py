# tests/test_cli.py

"""
Unit tests for the CLI class.
"""

import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from labmateai.cli import CLI


# Sample tools for mocking the database
SAMPLE_TOOLS = [
    (101, 'Seurat', 'Single-Cell Analysis', 'feature1;feature2', 'Free',
     'An R package for single-cell RNA sequencing data.', 'R', 'Cross-platform'),
    (102, 'Scanpy', 'Single-Cell Analysis', 'feature2;feature3', 'Free',
     'A scalable toolkit for analyzing single-cell gene expression data.', 'Python', 'Cross-platform'),
    (103, 'GenomicsToolX', 'Genomics', 'Genome Assembly;Variant Calling', 'Free',
     'A tool for comprehensive genome assembly and variant calling.', 'Python', 'Cross-platform'),
    (104, 'Bowtie', 'Genomics', 'Sequence Alignment;Genome Mapping', 'Free',
     'A fast and memory-efficient tool for aligning sequencing reads to long reference sequences.', 'C++', 'Cross-platform'),
    (105, 'RNAAnalyzer', 'RNA', 'RNA-Seq Analysis;Differential Expression', 'Free',
     'A tool for analyzing RNA-Seq data and identifying differential gene expression.', 'R', 'Cross-platform')
]


@pytest.fixture
def mock_cli():
    """
    Fixture to provide a mock CLI instance.
    """
    cli = CLI(db_path=':memory:')
    conn = sqlite3.connect(cli.db_path)
    cursor = conn.cursor()

    # Create users and tools tables
    cursor.execute('''
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        email TEXT UNIQUE,
        department TEXT,
        role TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE tools (
        tool_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        features TEXT,
        cost TEXT,
        description TEXT,
        language TEXT,
        platform TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE interactions (
        interaction_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tool_id INTEGER,
        rating INTEGER,
        usage_frequency TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (tool_id) REFERENCES tools(tool_id)
    )
    ''')

    # Insert sample tools into the tools table
    cursor.executemany('''
    INSERT INTO tools (tool_id, name, category, features, cost, description, language, platform)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', SAMPLE_TOOLS)

    conn.commit()
    conn.close()
    return cli


@patch('builtins.input', side_effect=['new', 'John Doe', 'johndoe@example.com', 'Biology', 'Researcher', '4'])
@patch('builtins.print')
def test_user_signup(mock_print, mock_input, mock_cli):
    """
    Test the signup process for a new user.
    """
    mock_cli.start()
    conn = sqlite3.connect(mock_cli.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?",
                   ('johndoe@example.com',))
    user = cursor.fetchone()
    assert user is not None, "User should be created in the database."
    assert user[1] == 'John Doe', "User name should match."
    assert user[2] == 'johndoe@example.com', "User email should match."
    conn.close()


@patch('builtins.input', side_effect=['existing', 'johndoe@example.com', '4'])
@patch('builtins.print')
def test_user_login(mock_print, mock_input, mock_cli):
    """
    Test the login process for an existing user.
    """
    # Pre-create a user in the database
    conn = sqlite3.connect(mock_cli.db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (user_name, email, department, role)
    VALUES (?, ?, ?, ?)
    ''', ('John Doe', 'johndoe@example.com', 'Biology', 'Researcher'))
    conn.commit()
    conn.close()

    mock_cli.start()
    # If no exceptions are raised, login was successful


@patch('builtins.input', side_effect=['1', 'Seurat', '3', '4'])
@patch('builtins.print')
def test_recommend_similar_tools(mock_print, mock_input, mock_cli):
    """
    Test recommending similar tools based on a tool name.
    """
    mock_cli.start()
    mock_print.assert_any_call("\nRecommendations:")
    mock_print.assert_any_call(
        "- Scanpy (ID: 102): A scalable toolkit for analyzing single-cell gene expression data. (Cost: Free)")


@patch('builtins.input', side_effect=['2', 'Single-Cell Analysis', '2', '4'])
@patch('builtins.print')
def test_recommend_tools_in_category(mock_print, mock_input, mock_cli):
    """
    Test recommending tools within a specified category.
    """
    mock_cli.start()
    mock_print.assert_any_call("\nRecommendations:")
    mock_print.assert_any_call(
        "- Seurat (ID: 101): An R package for single-cell RNA sequencing data. (Cost: Free)")
    mock_print.assert_any_call(
        "- Scanpy (ID: 102): A scalable toolkit for analyzing single-cell gene expression data. (Cost: Free)")


@patch('builtins.input', side_effect=['3', 'RNA', '3', '4'])
@patch('builtins.print')
def test_search_tools_by_keyword(mock_print, mock_input, mock_cli):
    """
    Test searching tools by a keyword.
    """
    mock_cli.start()
    mock_print.assert_any_call("\nRecommendations:")
    mock_print.assert_any_call(
        "- RNAAnalyzer (ID: 105): A tool for analyzing RNA-Seq data and identifying differential gene expression. (Cost: Free)")


@patch('builtins.input', side_effect=['4', '101', '5'])
@patch('builtins.print')
def test_rate_recommendation(mock_print, mock_input, mock_cli):
    """
    Test rating a recommended tool.
    """
    # Pre-create a user in the database
    conn = sqlite3.connect(mock_cli.db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (user_name, email, department, role)
    VALUES (?, ?, ?, ?)
    ''', ('Jane Doe', 'janedoe@example.com', 'Chemistry', 'Student'))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    mock_cli.start()

    # Verify the rating was logged
    conn = sqlite3.connect(mock_cli.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM interactions WHERE user_id = ? AND tool_id = ?", (user_id, 101))
    interaction = cursor.fetchone()
    assert interaction is not None, "Interaction should be logged in the database."
    assert interaction[3] == 5, "Rating should be 5."
    conn.close()


@patch('builtins.input', side_effect=['1', 'NonExistentTool', '4'])
@patch('builtins.print')
def test_nonexistent_tool_recommendation(mock_print, mock_input, mock_cli):
    """
    Test the behavior when a non-existent tool is provided for recommendations.
    """
    mock_cli.start()
    mock_print.assert_any_call("Tool 'NonExistentTool' not found.")
