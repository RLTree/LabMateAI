# tests/test_hybrid_recommender.py

import pytest
from unittest.mock import patch
import pandas as pd
from labmateai.recommender import Recommender
from labmateai.collaborative_recommender import CollaborativeRecommender
from labmateai.hybrid_recommender import HybridRecommender
from labmateai.tool import Tool

# Sample data for testing
SAMPLE_TOOLS = [
    Tool(tool_id=101, name='ToolA', category='CategoryA', features=['feature1', 'feature2'], cost='Free',
         description='Description A', url='http://example.com/a', language='Python', platform='Cross-platform'),
    Tool(tool_id=102, name='ToolB', category='CategoryB', features=['feature2', 'feature3'], cost='Free',
         description='Description B', url='http://example.com/b', language='Python', platform='Cross-platform'),
    Tool(tool_id=103, name='ToolC', category='CategoryC', features=['feature1', 'feature3'], cost='Free',
         description='Description C', url='http://example.com/c', language='R', platform='Linux'),
]

SAMPLE_USER_ITEM_MATRIX = pd.DataFrame(
    {
        101: [5, 0, 3],  # Ratings for ToolA
        102: [0, 4, 2],  # Ratings for ToolB
        103: [0, 0, 5],  # Ratings for ToolC
    },
    index=[1, 2, 3]  # User IDs
)

SAMPLE_TOOLS_DF = pd.DataFrame(
    [
        {'tool_id': 101, 'name': 'ToolA', 'category': 'CategoryA', 'features': 'feature1;feature2', 'cost': 'Free',
         'description': 'Description A', 'url': 'http://example.com/a', 'language': 'Python', 'platform': 'Cross-platform'},
        {'tool_id': 102, 'name': 'ToolB', 'category': 'CategoryB', 'features': 'feature2;feature3', 'cost': 'Free',
         'description': 'Description B', 'url': 'http://example.com/b', 'language': 'Python', 'platform': 'Cross-platform'},
        {'tool_id': 103, 'name': 'ToolC', 'category': 'CategoryC', 'features': 'feature1;feature3', 'cost': 'Free',
         'description': 'Description C', 'url': 'http://example.com/c', 'language': 'R', 'platform': 'Linux'},
    ]
)


@pytest.fixture
def content_recommender():
    """Fixture to provide a content-based Recommender instance."""
    return Recommender(tools=[tool for tool in SAMPLE_TOOLS])


@pytest.fixture
def collaborative_recommender():
    """Fixture to provide a collaborative-based CollaborativeRecommender instance."""
    return CollaborativeRecommender(user_item_matrix=SAMPLE_USER_ITEM_MATRIX, tools_df=SAMPLE_TOOLS_DF, n_neighbors=2)


@pytest.fixture
def hybrid_recommender(content_recommender, collaborative_recommender):
    """Fixture to provide a HybridRecommender instance."""
    return HybridRecommender(content_recommender=content_recommender,
                             collaborative_recommender=collaborative_recommender, alpha=0.5)


def test_hybrid_recommender_with_valid_user(hybrid_recommender):
    """Test the hybrid recommender with a valid user ID."""
    user_id = 1
    recommendations = hybrid_recommender.recommend(
        user_id=user_id, num_recommendations=3)
    assert len(recommendations) <= 3
    assert all('tool_id' in recommendation for recommendation in recommendations)
    assert all('tool_name' in recommendation for recommendation in recommendations)
    print("Test passed: Hybrid recommender returns valid recommendations.")


def test_hybrid_recommender_no_ratings_user(hybrid_recommender):
    """Test hybrid recommender for a user with no ratings."""
    user_id = 4  # User ID not present in user-item matrix
    with pytest.raises(ValueError, match=f"User ID {user_id} not found in the user-item matrix."):
        hybrid_recommender.recommend(user_id=user_id, num_recommendations=3)


def test_hybrid_recommender_with_content_based_filtering(hybrid_recommender):
    """Test hybrid recommender with content-based filtering involved."""
    user_id = 1
    tool_name = 'ToolA'
    recommendations = hybrid_recommender.recommend(
        user_id=user_id, tool_name=tool_name, num_recommendations=3)
    assert len(recommendations) <= 3
    assert all(isinstance(recommendation, dict)
               for recommendation in recommendations)
    print("Test passed: Hybrid recommender returns combined collaborative and content-based recommendations.")


def test_hybrid_recommender_with_high_alpha(hybrid_recommender):
    """Test hybrid recommender with high alpha (favoring CF)."""
    hybrid_recommender.alpha = 0.9
    user_id = 2
    recommendations = hybrid_recommender.recommend(
        user_id=user_id, num_recommendations=3)
    assert len(recommendations) <= 3
    print("Test passed: Hybrid recommender works with high alpha.")


def test_hybrid_recommender_with_low_alpha(hybrid_recommender):
    """Test hybrid recommender with low alpha (favoring CBF)."""
    hybrid_recommender.alpha = 0.1
    user_id = 3
    tool_name = 'ToolB'
    recommendations = hybrid_recommender.recommend(
        user_id=user_id, tool_name=tool_name, num_recommendations=3)
    assert len(recommendations) <= 3
    print("Test passed: Hybrid recommender works with low alpha.")


def test_hybrid_recommender_no_tool_name(hybrid_recommender):
    """Test hybrid recommender without content-based tool name input."""
    user_id = 1
    recommendations = hybrid_recommender.recommend(
        user_id=user_id, num_recommendations=2)
    assert len(recommendations) <= 2
    assert all(isinstance(recommendation, dict)
               for recommendation in recommendations)
    print("Test passed: Hybrid recommender works without content-based input.")


def test_hybrid_recommender_invalid_alpha(hybrid_recommender):
    """Test hybrid recommender with an invalid alpha value."""
    hybrid_recommender.alpha = 1.5  # Invalid alpha
    user_id = 1
    with pytest.raises(ValueError, match="Alpha must be between 0 and 1"):
        hybrid_recommender.recommend(user_id=user_id, num_recommendations=2)


@pytest.mark.parametrize("num_recommendations", [0, -1, 100])
def test_hybrid_recommender_edge_cases_num_recommendations(hybrid_recommender, num_recommendations):
    """Test hybrid recommender with edge cases for num_recommendations."""
    user_id = 1
    if num_recommendations <= 0:
        with pytest.raises(ValueError, match="n_recommendations must be at least 1."):
            hybrid_recommender.recommend(
                user_id=user_id, num_recommendations=num_recommendations)
    else:
        recommendations = hybrid_recommender.recommend(
            user_id=user_id, num_recommendations=num_recommendations)
        assert len(recommendations) <= len(SAMPLE_TOOLS)
        print(
            f"Test passed: Hybrid recommender works with {num_recommendations} recommendations.")


if __name__ == "__main__":
    pytest.main()
