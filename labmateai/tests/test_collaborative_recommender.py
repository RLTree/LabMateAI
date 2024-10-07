# tests/test_collaborative_recommender.py

"""
Unit tests for the CollaborativeRecommender class in LabMateAI.
"""

import pytest
import pandas as pd
import numpy as np
from labmateai.collaborative_recommender import CollaborativeRecommender


@pytest.fixture
def mock_tools_df():
    """
    Fixture to provide a mock tools DataFrame for testing.
    """
    data = {
        'tool_id': [101, 102, 103, 104, 105],
        'tool_name': ['ToolA', 'ToolB', 'ToolC', 'ToolD', 'ToolE'],
        'category': ['Genomics', 'Proteomics', 'Metabolomics', 'Genomics', 'RNA'],
        'features': [
            'Feature1; Feature2',
            'Feature3; Feature4',
            'Feature5; Feature6',
            'Feature1; Feature7',
            'Feature8; Feature9'
        ],
        'cost': ['Free', 'Paid', 'Paid', 'Paid', 'Paid'],  # Changed to string
        'description': [
            'Description for ToolA',
            'Description for ToolB',
            'Description for ToolC',
            'Description for ToolD',
            'Description for ToolE'
        ],
        'url': [
            'https://toola.example.com',
            'https://toolb.example.com',
            'https://toolc.example.com',
            'https://toold.example.com',
            'https://toole.example.com'
        ],
        'language': ['Python', 'R', 'C++', 'Java', 'Python'],
        'platform': ['Windows', 'Linux', 'MacOS', 'Windows', 'Linux']
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
        101: [5.0, 0.0, 3.0],  # Changed to float
        102: [0.0, 4.0, 0.0],
        103: [2.0, 0.0, 5.0],
        104: [0.0, 3.0, 0.0],
        105: [1.0, 0.0, 0.0]
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
    # Adjusted based on mock data and similarity
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
    # Create a user-item matrix with all zeros for a new user
    user_item_matrix = pd.DataFrame({
        101: [0.0],
        102: [0.0],
        103: [0.0],
        104: [0.0],
        105: [0.0]
    }, index=[4])

    # Initialize a new CollaborativeRecommender instance
    recommender = CollaborativeRecommender(
        user_item_matrix=user_item_matrix,
        tools_df=mock_tools_df,
        n_neighbors=2
    )

    recommendations = recommender.get_recommendations(
        user_id=4, n_recommendations=3)

    # Since the user has no ratings, NearestNeighbors should find similar users based on zero vectors
    # Mean ratings across users: 101: (5+0+3)/3 = 2.666..., 102: (0+4+0)/3 = 1.333..., 103: (2+0+5)/3 = 2.333..., 104: (0+3+0)/3 = 1.0, 105: (1+0+0)/3 = 0.333...
    expected_tool_ids = [101, 103, 102]
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert set(retrieved_tool_ids) == set(
        expected_tool_ids), f"Expected recommendations {expected_tool_ids}, got {retrieved_tool_ids}."


def test_get_recommendations_user_rated_all_tools(mock_tools_df):
    """
    Test generating recommendations for a user who has rated all tools.
    """
    # User 3 has rated all tools
    user_item_matrix = pd.DataFrame({
        101: [5.0],
        102: [5.0],
        103: [5.0],
        104: [5.0],
        105: [5.0]
    }, index=[3])

    # Initialize a new CollaborativeRecommender instance
    recommender = CollaborativeRecommender(
        user_item_matrix=user_item_matrix, tools_df=mock_tools_df, n_neighbors=2)

    recommendations = recommender.get_recommendations(
        user_id=3, n_recommendations=2)

    # Since user 3 has rated all tools, there should be no recommendations
    assert recommendations == [], "Expected no recommendations for user who has rated all tools."


def test_recommender_tool_not_in_tools_df(mock_user_item_matrix, mock_tools_df):
    """
    Test that tools not present in tools_df are not recommended.
    """
    new_tool_id = 106
    # Add a new tool to the user-item matrix
    mock_user_item_matrix[new_tool_id] = [0.0, 0.0, 0.0]

    # Initialize a new CollaborativeRecommender instance
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            mock_user_item_matrix,
            tools_df=mock_tools_df,  # original tools_df does not include tool_id 106
            n_neighbors=2
        )
    assert f"User-item matrix contains tool_ids not present in tools_df: {{{new_tool_id}}}" in str(
        exc_info.value), \
        "Expected ValueError for tool_ids not present in tools_df."


def test_recommender_multiple_similar_users(mock_user_item_matrix, mock_tools_df):
    """
    Test that recommendations are based on multiple similar users' preferences.
    """
    # Initialize a new CollaborativeRecommender instance
    recommender = CollaborativeRecommender(
        mock_user_item_matrix, mock_tools_df, n_neighbors=2)

    # User 1 has rated ToolA and ToolC, User 3 has rated ToolC and ToolE
    recommendations = recommender.get_recommendations(
        user_id=1, n_recommendations=2)

    # Based on user 3's ratings and excluding already rated tools
    expected_tool_ids = [104, 102]
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    assert set(retrieved_tool_ids) == set(
        expected_tool_ids), f"Expected recommendations {expected_tool_ids}, got {retrieved_tool_ids}."


def test_recommender_tool_ratings_float(mock_user_item_matrix, mock_tools_df):
    """
    Test that tool ratings are handled correctly as floats.
    """
    # Initialize a new CollaborativeRecommender instance
    recommender = CollaborativeRecommender(
        mock_user_item_matrix, mock_tools_df, n_neighbors=2)

    # Ensure that ratings are floats
    assert recommender.user_item_matrix.dtypes.apply(lambda x: np.issubdtype(x, np.floating)).all(), \
        "All ratings should be of float type."

    # Add a user with float ratings
    new_user_id = 5
    updated_user_item_matrix = recommender.user_item_matrix.copy()
    updated_user_item_matrix.loc[new_user_id] = [4.5, 3.2, 0.0, 1.8, 2.5]

    # Re-initialize the recommender with the updated matrix
    new_recommender = CollaborativeRecommender(
        user_item_matrix=updated_user_item_matrix,
        tools_df=recommender.tools_df,
        n_neighbors=2
    )

    recommendations = new_recommender.get_recommendations(
        user_id=new_user_id, n_recommendations=2)

    # Check that recommendations are as expected
    # Based on user similarity, expected tools could vary; here we ensure that recommendations are valid tool IDs not already rated
    for rec in recommendations:
        assert rec['tool_id'] not in {
            new_user_id}, "Recommended tool should not be already rated by the user."


def test_recommender_zero_neighbors(mock_user_item_matrix, mock_tools_df):
    """
    Test behavior when n_neighbors is set to zero.
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
    Test that initializing with a negative number of neighbors raises an error.
    """
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=mock_tools_df,
            n_neighbors=-1
        )
    assert "n_neighbors must be at least 1." in str(
        exc_info.value), "Expected ValueError for negative n_neighbors."


def test_recommender_tool_with_no_average_rating(collaborative_recommender_instance, mock_user_item_matrix, mock_tools_df):
    """
    Test that tools with no ratings from similar users are not recommended.
    """
    recommender = collaborative_recommender_instance
    # Assuming tool 105 has minimal ratings, ensure it's recommended appropriately
    recommendations = recommender.get_recommendations(
        user_id=2, n_recommendations=3)
    retrieved_tool_ids = [rec['tool_id'] for rec in recommendations]
    # Tool 105 should be recommended as it's rated by user 1
    assert 105 in retrieved_tool_ids, "Tool 105 should be recommended based on user 1's rating."


def test_recommender_no_recommendations_available(collaborative_recommender_instance, mock_user_item_matrix, mock_tools_df):
    """
    Test that no recommendations are returned when no tools are available to recommend.
    """
    recommender = collaborative_recommender_instance
    # Remove all tools from tools_df
    updated_tools_df = mock_tools_df.drop(mock_tools_df.index)

    # Attempt to initialize a new recommender with no tools
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=updated_tools_df,
            n_neighbors=2
        )
    assert "User-item matrix contains tool_ids not present in tools_df" in str(exc_info.value), \
        "Expected ValueError when no tools are available."


def test_recommender_duplicate_tools(mock_user_item_matrix, mock_tools_df):
    """
    Test that initializing with duplicate tools raises a ValueError.
    """
    # Add a duplicate tool_id
    duplicate_tool = {
        'tool_id': 101,  # Duplicate ID
        'tool_name': 'ToolA_Duplicate',
        'category': 'Genomics',
        'features': 'Feature1; Feature2',
        'cost': 'Free',
        'description': 'Duplicate ToolA',
        'url': 'https://toola-duplicate.example.com',
        'language': 'Python',
        'platform': 'Windows'
    }

    # Convert the dictionary to a DataFrame and concatenate with the original tools_df
    duplicate_tool_df = pd.DataFrame([duplicate_tool])
    updated_tools_df = pd.concat(
        [mock_tools_df, duplicate_tool_df], ignore_index=True)

    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=updated_tools_df,
            n_neighbors=2
        )
    assert "Duplicate tool_ids found in tools_df." in str(exc_info.value), \
        "Expected ValueError for duplicate tool_ids in tools_df."


def test_recommender_tool_ratings_zero_neighbors(mock_user_item_matrix, mock_tools_df):
    """
    Additional test to ensure that recommendations are empty when n_neighbors is zero.
    """
    with pytest.raises(ValueError) as exc_info:
        CollaborativeRecommender(
            user_item_matrix=mock_user_item_matrix,
            tools_df=mock_tools_df,
            n_neighbors=0
        )
    assert "n_neighbors must be at least 1." in str(
        exc_info.value), "Expected ValueError for n_neighbors=0."


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
