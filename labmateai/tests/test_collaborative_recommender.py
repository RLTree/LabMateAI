# tests/test_collaborative_recommender.py

"""
Unit tests for the CollaborativeRecommender class in LabMateAI.
"""

import pytest
import pandas as pd
from labmateai.collaborative_recommender import CollaborativeRecommender


@pytest.fixture
def mock_tools_df():
    """
    Fixture to provide a mock tools DataFrame for testing.
    """
    data = {
        'tool_id': [101, 102, 103, 104, 105],
        'tool_name': ['Seurat', 'Scanpy', 'RNAAnalyzer', 'ToolD', 'ToolE'],
        'category': ['Single-Cell Analysis', 'Single-Cell Analysis', 'RNA', 'Genomics', 'Proteomics'],
        'features': [
            'Feature1; Feature2',
            'Feature1; Feature3',
            'Feature1; Feature4',
            'Feature5; Feature6',
            'Feature7; Feature8'
        ],
        'cost': ['Free', 'Free', 'Paid', 'Paid', 'Paid'],
        'description': [
            'Description for Seurat',
            'Description for Scanpy',
            'Description for RNAAnalyzer',
            'Description for ToolD',
            'Description for ToolE'
        ],
        'url': [
            'https://seurat.example.com',
            'https://scanpy.example.com',
            'https://rnaanalyzer.example.com',
            'https://toold.example.com',
            'https://toole.example.com'
        ],
        'language': ['R', 'Python', 'R', 'Java', 'Python'],
        'platform': ['Cross-platform', 'Cross-platform', 'Cross-platform', 'Linux', 'Windows']
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_user_item_matrix():
    """
    Fixture to provide a mock user-item matrix for testing.
    Users: 1, 2, 3
    Tools: 101, 102, 103, 104, 105
    Ratings range from 1 to 5, with 0 indicating no interaction.
    """
    data = {
        101: [5.0, 0.0, 3.0],  # Ratings for Seurat
        102: [0.0, 4.0, 0.0],  # Ratings for Scanpy
        103: [2.0, 0.0, 5.0],  # Ratings for RNAAnalyzer
        104: [0.0, 3.0, 0.0],  # Ratings for ToolD
        105: [1.0, 0.0, 0.0]   # Ratings for ToolE
    }
    return pd.DataFrame(data, index=[1, 2, 3])


@pytest.fixture
def collaborative_recommender_instance(mock_user_item_matrix, mock_tools_df):
    """
    Fixture to provide a CollaborativeRecommender instance initialized with mock data.
    """
    return CollaborativeRecommender(
        user_item_matrix=mock_user_item_matrix,
        tools_df=mock_tools_df,
        n_neighbors=2
    )


def test_collaborative_recommender_initialization(collaborative_recommender_instance, mock_user_item_matrix, mock_tools_df):
    """
    Test that the CollaborativeRecommender initializes correctly with provided data.
    """
    recommender = collaborative_recommender_instance
    assert isinstance(recommender.model, CollaborativeRecommender.__bases__[
                      0]), "NearestNeighbors model not initialized correctly."
    assert recommender.user_item_matrix.equals(
        mock_user_item_matrix), "User-item matrix not stored correctly."
    assert recommender.tools_df.equals(
        mock_tools_df), "Tools DataFrame not stored correctly."
    assert recommender.n_neighbors == 2, "Number of neighbors not set correctly."
    assert recommender.tool_id_to_details == mock_tools_df.set_index(
        'tool_id').to_dict('index'), "Tool ID to details mapping incorrect."
    assert recommender.all_tool_ids == set(
        [101, 102, 103, 104, 105]), "All tool IDs not captured correctly."


def test_get_recommendations_valid_user(collaborative_recommender_instance):
    """
    Test generating recommendations for a valid user with existing ratings.
    """
    recommender = collaborative_recommender_instance
    recommendations = recommender.get_recommendations(
        user_id=1, n_recommendations=2)
    expected_tool_ids = [102, 104]
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert retrieved_tool_ids == expected_tool_ids, f"Expected recommendations {expected_tool_ids}, got {retrieved_tool_ids}."


def test_get_recommendations_invalid_user(collaborative_recommender_instance):
    """
    Test that providing an invalid user_id raises a ValueError.
    """
    recommender = collaborative_recommender_instance
    with pytest.raises(ValueError) as exc_info:
        recommender.get_recommendations(user_id=999, n_recommendations=2)
    assert "User ID 999 not found in the user-item matrix." in str(
        exc_info.value), "Expected ValueError for invalid user_id."


def test_get_recommendations_user_with_no_ratings(mock_tools_df):
    """
    Test generating recommendations for a user with no ratings.
    """
    user_item_matrix = pd.DataFrame({
        101: [0.0],
        102: [0.0],
        103: [0.0],
        104: [0.0],
        105: [0.0]
    }, index=[4])

    recommender = CollaborativeRecommender(
        user_item_matrix=user_item_matrix,
        tools_df=mock_tools_df,
        n_neighbors=1
    )

    recommendations = recommender.get_recommendations(
        user_id=4, n_recommendations=3)
    expected_tool_ids = [101, 102, 103]
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert set(retrieved_tool_ids) == set(
        expected_tool_ids), f"Expected recommendations {expected_tool_ids}, got {retrieved_tool_ids}."


def test_get_recommendations_user_rated_all_tools(mock_tools_df):
    """
    Test generating recommendations for a user who has rated all tools.
    """
    user_item_matrix = pd.DataFrame({
        101: [5.0],
        102: [5.0],
        103: [5.0],
        104: [5.0],
        105: [5.0]
    }, index=[3])

    recommender = CollaborativeRecommender(
        user_item_matrix=user_item_matrix, tools_df=mock_tools_df, n_neighbors=1)

    recommendations = recommender.get_recommendations(
        user_id=3, n_recommendations=2)
    assert recommendations == [], "Expected no recommendations for user who has rated all tools."


def test_recommender_tool_not_in_tools_df(mock_user_item_matrix, mock_tools_df):
    """
    Test that providing a tool_id not present in tools_df raises a ValueError.
    """
    new_tool_id = 106
    mock_user_item_matrix[new_tool_id] = [0.0, 0.0, 0.0]

    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            mock_user_item_matrix,
            tools_df=mock_tools_df,
            n_neighbors=2
        )
    assert f"User-item matrix contains tool_ids not present in tools_df: {{{new_tool_id}}}" in str(exc_info.value), \
        "Expected ValueError for tool_ids not present in tools_df."


def test_recommender_multiple_similar_users(mock_user_item_matrix, mock_tools_df):
    """
    Test generating recommendations when multiple similar users are available.
    """
    recommender = CollaborativeRecommender(
        mock_user_item_matrix, mock_tools_df, n_neighbors=2)
    recommendations = recommender.get_recommendations(
        user_id=1, n_recommendations=2)
    expected_tool_ids = [102, 104]
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert set(retrieved_tool_ids) == set(
        expected_tool_ids), f"Expected recommendations {expected_tool_ids}, got {retrieved_tool_ids}."


def test_recommender_zero_neighbors(mock_user_item_matrix, mock_tools_df):
    """
    Test that providing n_neighbors=0 raises a ValueError.
    """
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=mock_tools_df,
            n_neighbors=0
        )
    assert "n_neighbors must be at least 1." in str(
        exc_info.value), "Expected ValueError for n_neighbors=0."


def test_recommender_negative_neighbors(mock_user_item_matrix, mock_tools_df):
    """
    Test that providing n_neighbors=-1 raises a ValueError.
    """
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=mock_tools_df,
            n_neighbors=-1
        )
    assert "n_neighbors must be at least 1." in str(
        exc_info.value), "Expected ValueError for negative n_neighbors."


def test_recommender_excludes_already_rated_tools(collaborative_recommender_instance, mock_user_item_matrix):
    """
    Test that recommendations exclude tools already rated by the user.
    """
    recommender = collaborative_recommender_instance
    user_id = 1
    user_rated_tools = set(
        mock_user_item_matrix.loc[user_id][mock_user_item_matrix.loc[user_id] > 0].index)
    recommendations = recommender.get_recommendations(
        user_id=user_id, n_recommendations=5)
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert not user_rated_tools.intersection(
        retrieved_tool_ids), "Recommendations should not include tools already rated by the user."
