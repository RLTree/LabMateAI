# tests/test_data_loader.py

"""
Unit tests for the data_loader module using the PostgreSQL database.
"""

import pytest
from unittest.mock import patch, MagicMock
from labmateai.data_loader import load_tools_from_db, load_users_from_db, load_interactions_from_db
from labmateai.tool import Tool

# Sample data for mocking database response
SAMPLE_TOOLS_DB_ROWS = [
    (119, 'Seurat', 'Single-Cell Analysis', 'Single-cell RNA-seq;Clustering', 'Free',
     'An R package for single-cell RNA sequencing data.', 'https://satijalab.org/seurat/', 'R', 'Cross-platform'),
    (359, 'GenomicsToolX', 'Genomics', 'Genome Assembly;Variant Calling', 'Free',
     'A tool for comprehensive genome assembly and variant calling.', 'https://genomicstoolx.com/', 'Python', 'Cross-platform'),
    (360, 'RNAAnalyzer', 'RNA', 'RNA-Seq Analysis;Differential Expression', 'Free',
     'A tool for analyzing RNA-Seq data and identifying differential gene expression.', 'https://rnaanalyzer.example.com/', 'R', 'Cross-platform')
]

SAMPLE_USERS_DB_ROWS = [
    (1, 'Alice', 'alice@example.com', 'Biology', 'Researcher'),
    (2, 'Bob', 'bob@example.com', 'Genomics', 'Scientist'),
    (3, 'Charlie', 'charlie@example.com', 'Bioinformatics', 'Lab Manager')
]

SAMPLE_INTERACTIONS_DB_ROWS = [
    (1, 1, 119, 5, 'Daily', '2023-09-15 12:34:56'),
    (2, 2, 359, 4, 'Weekly', '2023-09-16 09:15:32'),
    (3, 3, 360, 3, 'Monthly', '2023-09-17 14:22:45')
]


@patch('psycopg2.connect')
def test_load_tools_from_db_success(mock_connect):
    """
    Test successful loading of tools from the PostgreSQL database.

    Args:
        mock_connect: Mock for psycopg2.connect.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the fetchall to return sample data
    mock_cursor.fetchall.return_value = SAMPLE_TOOLS_DB_ROWS

    # Call the function and validate results
    tools = load_tools_from_db()
    assert len(tools) == len(
        SAMPLE_TOOLS_DB_ROWS), f"Expected {len(SAMPLE_TOOLS_DB_ROWS)} tools, got {len(tools)}."

    for tool, expected_row in zip(tools, SAMPLE_TOOLS_DB_ROWS):
        assert tool.tool_id == expected_row[
            0], f"Expected tool_id '{expected_row[0]}', got '{tool.tool_id}'."
        assert tool.name == expected_row[
            1], f"Expected tool name '{expected_row[1]}', got '{tool.name}'."
        assert tool.category == expected_row[
            2], f"Expected category '{expected_row[2]}', got '{tool.category}'."
        assert tool.features == [feature.strip().lower() for feature in expected_row[3].split(';') if feature.strip()], \
            f"Expected features '{expected_row[3]}', got '{tool.features}'."
        assert tool.cost == expected_row[4], f"Expected cost '{expected_row[4]}', got '{tool.cost}'."
        assert tool.description == expected_row[
            5], f"Expected description '{expected_row[5]}', got '{tool.description}'."
        assert tool.url == expected_row[6], f"Expected URL '{expected_row[6]}', got '{tool.url}'."
        assert tool.language == expected_row[
            7], f"Expected language '{expected_row[7]}', got '{tool.language}'."
        assert tool.platform == expected_row[
            8], f"Expected platform '{expected_row[8]}', got '{tool.platform}'."


@patch('psycopg2.connect')
def test_load_users_from_db_success(mock_connect):
    """
    Test successful loading of users from the PostgreSQL database.

    Args:
        mock_connect: Mock for psycopg2.connect.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the fetchall to return sample data
    mock_cursor.fetchall.return_value = SAMPLE_USERS_DB_ROWS

    # Call the function and validate results
    users = load_users_from_db()
    assert len(users) == len(
        SAMPLE_USERS_DB_ROWS), f"Expected {len(SAMPLE_USERS_DB_ROWS)} users, got {len(users)}."

    for user, expected_row in zip(users, SAMPLE_USERS_DB_ROWS):
        assert user['user_id'] == expected_row[
            0], f"Expected user_id '{expected_row[0]}', got '{user['user_id']}'."
        assert user['user_name'] == expected_row[
            1], f"Expected user_name '{expected_row[1]}', got '{user['user_name']}'."
        assert user['email'] == expected_row[
            2], f"Expected email '{expected_row[2]}', got '{user['email']}'."
        assert user['department'] == expected_row[
            3], f"Expected department '{expected_row[3]}', got '{user['department']}'."
        assert user['role'] == expected_row[
            4], f"Expected role '{expected_row[4]}', got '{user['role']}'."


@patch('psycopg2.connect')
def test_load_interactions_from_db_success(mock_connect):
    """
    Test successful loading of interactions from the PostgreSQL database.

    Args:
        mock_connect: Mock for psycopg2.connect.
    """
    # Setup the mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock the fetchall to return sample data
    mock_cursor.fetchall.return_value = SAMPLE_INTERACTIONS_DB_ROWS

    # Call the function and validate results
    interactions = load_interactions_from_db()
    assert len(interactions) == len(
        SAMPLE_INTERACTIONS_DB_ROWS), f"Expected {len(SAMPLE_INTERACTIONS_DB_ROWS)} interactions, got {len(interactions)}."

    for interaction, expected_row in zip(interactions, SAMPLE_INTERACTIONS_DB_ROWS):
        assert interaction['interaction_id'] == expected_row[
            0], f"Expected interaction_id '{expected_row[0]}', got '{interaction['interaction_id']}'."
        assert interaction['user_id'] == expected_row[
            1], f"Expected user_id '{expected_row[1]}', got '{interaction['user_id']}'."
        assert interaction['tool_id'] == expected_row[
            2], f"Expected tool_id '{expected_row[2]}', got '{interaction['tool_id']}'."
        assert interaction['rating'] == expected_row[
            3], f"Expected rating '{expected_row[3]}', got '{interaction['rating']}'."
        assert interaction['usage_frequency'] == expected_row[
            4], f"Expected usage_frequency '{expected_row[4]}', got '{interaction['usage_frequency']}'."
        assert interaction['timestamp'] == expected_row[
            5], f"Expected timestamp '{expected_row[5]}', got '{interaction['timestamp']}'."
